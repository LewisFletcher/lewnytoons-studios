from django.views.generic.base import View
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.urls import reverse_lazy, reverse
import stripe
from django.conf import settings
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from .models import Price, Product, Order, Customer, FrequentlyAsked, SampleSong
from . import forms
from .forms import OrderForm
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, ListView
from .forms import CustomerUpdateForm, OrderUpdateForm
from django.utils.html import mark_safe
from django.db.models import Q
from datetime import datetime, timedelta

stripe.api_key = settings.STRIPE_SECRET_KEY

sidebar_context = {
    'sidebarhead' : 'Quick Find',
    'sidebar1' : 'LewnyToons - About',
    'sidebar2' : 'Services Offered',
    'sidebar3' : 'FAQ\'s',
    'sidebar4' : 'Before/After Examples',
    'sidebar5' : 'Contact',
    'sidebar6' : 'Tutor Session Portal',
    'sb1url' : '/music#about',
    'sb2url' : '/musicstudios#services',
    'sb3url' : '/musicstudios/frequently-asked-questions',
    'sb4url' : '/musicstudios/before-after',
    'sb5url' : '/musicstudios#contact',
    'sb6url' : '#',
}
 
def orderdetails(request):
    form = OrderForm()
    context = {'form' : form}
    context.update(sidebar_context)
    template_name = 'musicstudios/order_details.html'
    return render(request, template_name, context)

def prices(request):
    form = OrderForm(request.GET)
    return HttpResponse(form['price'])

def custupload(request):
    if request.POST:
        form = forms.CustomerForm(request.POST, request.FILES)
        success_url = reverse_lazy('orderdetails')
        if form.is_valid():
            customer = form.save()
            request.session['customer_id'] = customer.id
            print(request.session['customer_id'])
        else:
            ctx = {'form' : form}
            return render(request, 'musicstudios/customer_details.html', ctx)
        return HttpResponseRedirect(success_url)



def orderupload(request):
    if request.POST:
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            cust = request.session.get('customer_id') 
            instance.customer_id = cust
            instance.save(request)
            request.session['order_id'] = instance.id
            return redirect('order-review', instance.id)
        else:
            ctx = {'form' : form}
            return HttpResponseRedirect(request, 'musicstudios/order_details.html', ctx) 

def orderdelete(request):
    if request.session.get('customer_id') != None:
        instance = request.session.get('customer_id')
        customer = Customer.objects.get(id=instance)
        try:
            order = Order.objects.filter(customer_id=instance)[0]
            if order.status == True:
                return redirect('musicstudios')
            else:
                customer.delete()
                return redirect('musicstudios')
        except:
            customer.delete()
            return redirect('musicstudios')
    else:
        return redirect('musicstudios')
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_email = session["customer_details"]["email"]
        line_items = stripe.checkout.Session.list_line_items(session["id"])
        print(line_items)
        print(customer_email)
        stripe_price_id = line_items["data"][0]["price"]["id"]
        price = Price.objects.get(stripe_price_id=stripe_price_id)
        total_paid_cents = line_items["data"][0]["amount_total"]
        stripe_order_id = line_items["data"][0]["id"]
        total_paid_dollars = float(total_paid_cents / 100)
        print(total_paid_dollars)
        customer = Customer.objects.get(email= customer_email)
        order = Order.objects.get(customer = customer.id)
        order.status= True
        order.customer_paid = total_paid_dollars
        order.stripe_order_id = stripe_order_id
        current_time = datetime.now()
        order.fullfilment_date = current_time + timedelta(days = 7)
        order.save()

    #elif event['type'] == 'check'

        # TODO - send an email to the customer
    return HttpResponse(status=200)

class StudiosOverview(View):
    def get(self, request):
        products = Product.objects.all()
        price = Price.objects.all()
        context = {
            'page_headline' : 'Studio Services',
            "products" : products,
            "prices": price,
        }
        context.update(sidebar_context)
        return render(request, 'musicstudios/overview.html', context)

class FrequentQuestion(ListView):
    model = FrequentlyAsked
    template_name = "musicstudios/faq.html"
    extra_context = sidebar_context
    context_object_name = 'questions'

class BeforeAfter(ListView):
    model = SampleSong
    template_name = "musicstudios/before_after.html"
    extra_context = sidebar_context
    context_object_name = 'samples'


class CustomerDetails(CreateView):
    form_class = forms.CustomerForm
    template_name = 'musicstudios/customer_details.html'
    extra_context = sidebar_context
    

class OrderReview(DetailView):
    model = Order
    template_name = 'musicstudios/order_review.html'
    extra_context = sidebar_context

    def get(self, request, pk):
        order = Order.objects.get(id=pk)
        customer = Customer.objects.get(pk=order.customer_id)
        if order.status == True:
            return HttpResponseNotFound("Not found.")
        elif request.session['order_id'] != order.id:
            return HttpResponseNotFound("Not found.")
        elif request.session['customer_id'] != order.customer.id:
            return HttpResponseNotFound("Not found.")
        else:
            self.extra_context.update({'customer' : customer, 'order' : order})
            return render(request, self.template_name, self.extra_context)

class CustomerUpdate(UpdateView):
    form_class = forms.CustomerUpdateForm
    template_name = 'musicstudios/customer_update.html'
    
    def get(self, request, pk):
        order_id = request.session.get('order_id')
        order = Order.objects.get(id=order_id)
        customer = get_object_or_404(Customer, id=pk)
        form = CustomerUpdateForm(instance=customer)
        if order.status == True:
            return HttpResponseNotFound("Not found.")
        elif order.customer.id != customer.id:
            return HttpResponseNotFound("Not found.")
        elif request.session['customer_id'] != order.customer.id:
            return HttpResponseNotFound("Not found.")
        else:
            ctx = {'form': form, 'order_id' : order_id}
            ctx.update(sidebar_context)
            return render(request, self.template_name, ctx)

    def post(self, request, pk):
        customer = get_object_or_404(Customer, id=pk)
        form = CustomerUpdateForm(request.POST, instance=customer)
        if form.is_valid():
            form.save(commit=True)
            pk = request.session.get('order_id')
            return redirect('order-review', pk)
        else:
            ctx = {'form': form}
            return render(request, self.template, ctx)

class CustomerSelect(TemplateView):
    template_name = "musicstudios/enter_email.html"
    extra_context = sidebar_context

def begin_order(request):
        strval = request.GET.get('email', False)
        print(strval)
        if strval:
            customer = Customer.objects.get(email=strval)
            if customer != None:
                request.session['customer_id'] = customer.id
                print(customer.id)
                return HttpResponseRedirect(reverse('orderdetails'))
            else:
                return HttpResponse('Customer could not be found.')

class OrderUpdate(UpdateView):
    form_class = forms.OrderUpdateForm
    template_name = 'musicstudios/order_update.html'

    def get(self, request, pk):
        order_id = request.session.get('order_id')
        order = get_object_or_404(Order, id=pk)
        form = OrderUpdateForm(instance=order)
        if order.status == True:
            return HttpResponseNotFound("Not found.")
        elif request.session['order_id'] != order.id:
            return HttpResponseNotFound("Not found.")
        elif request.session['customer_id'] != order.customer.id:
            return HttpResponseNotFound("Not found.")
        else:
            ctx = {'form': form, 'order_id' : order_id}
            ctx.update(sidebar_context)
            return render(request, self.template_name, ctx)

    def post(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        form = OrderUpdateForm(request.POST, instance=order)
        if form.is_valid():
            form.save(commit=True)
            pk = request.session.get('order_id')
            return redirect('order-review', pk)
        else:
            ctx = {'form': form}
            ctx.update(sidebar_context)
            return render(request, self.template, ctx)

class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        order_id = self.kwargs['pk']
        order = Order.objects.get(id=order_id)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        domain = "https://lewnytoonsstudios.com"
        if settings.DEBUG:
            domain = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            payment_intent_data={
                'metadata' : {'order_id': order_id}
            },
            metadata={
                "order_id": order_id,
            },
            customer_email= order.customer.email,
            line_items=[
                {
                    
                    'price': order.price.stripe_price_id,
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=domain + '/musicstudios/success/',
            cancel_url=domain + '/musicstudios/cancel/',
            automatic_tax={'enabled': True},
        )
        return redirect(checkout_session.url, code=303)

class SuccessView(TemplateView):
    template_name = "musicstudios/success.html"
    extra_context = sidebar_context
    def get_context_data(self, **kwargs):
        context = super(SuccessView, self).get_context_data(**kwargs)
        order_id = self.request.session.get('order_id')
        order = Order.objects.filter(pk=order_id)[0]
        product_id = order.product.id
        product = Product.objects.get(pk=product_id)
        customer = Customer.objects.get(pk=order.customer.id)
        context['customer'] = customer
        context['product'] = product
        context['order'] = order
        return context

    #def stripe_webhook(request):

    

class CancelView(TemplateView):
    template_name = "musicstudios/cancel.html"
    extra_context = sidebar_context
    def get_context_data(self, **kwargs):
        context = super(CancelView, self).get_context_data(**kwargs)
        order_id = self.request.session.get('order_id')
        order = Order.objects.get(pk=order_id)
        customer = Customer.objects.get(pk=order.customer.id)
        product_id = order.product.id
        product = Product.objects.get(pk=product_id)
        context['customer'] = customer
        context['product'] = product
        context['order'] = order
        return context