from django.views.generic.base import View
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.urls import reverse_lazy, reverse
import stripe
from django.conf import settings
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .models import Price, Product, Order, Customer
from . import forms
from .forms import OrderForm
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView
from .forms import CustomerUpdateForm, OrderUpdateForm

stripe.api_key = settings.STRIPE_SECRET_KEY

sidebar_context = {
    'sidebarhead' : 'Quick Find',
    'sidebar1' : 'LewnyToons - About',
    'sidebar2' : 'Services Offered',
    'sidebar3' : 'FAQ\'s',
    'sidebar4' : 'Before/After Examples',
    'sidebar5' : 'Feature Request',
    'sidebar6' : 'Tutor Request',
    'sb1url' : '/music#about',
    'sb2url' : '/studios#services',
    'sb3url' : '#',
    'sb4url' : '#',
    'sb5url' : '#',
    'sb6url' : '#',
}
 
def orderdetails(request):
    form = OrderForm()
    context = {'form' : form}
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
            return HttpResponseRedirect(request, 'musicstudios/customer_details.html', ctx)
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
        customer = Customer.objects.filter(id=instance)
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
        stripe_price_id = line_items["data"][0]["price"]["id"]
        price = Price.objects.get(stripe_price_id=stripe_price_id)
        total_paid_cents = line_items["data"][0]["amount_total"]
        total_paid_dollars = total_paid_cents / 100
        request.session['total_paid'] = total_paid_dollars
        #order_id = request.session.get('order_id')
        #order = Order.objects.get(id=order_id)
        #order.status = True
        #order.save()
        #print(order.status)

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


class CustomerDetails(CreateView):
    form_class = forms.CustomerForm
    template_name = 'musicstudios/customer_details.html'
    
stripe.api_key = settings.STRIPE_SECRET_KEY

class OrderReview(DetailView):
    model = Order
    template_name = 'musicstudios/order_review.html'
    extra_context = sidebar_context
    def get_context_data(self, **kwargs):
        context = super(OrderReview, self).get_context_data(**kwargs)
        order = self.get_object()
        customer = Customer.objects.get(pk=order.customer_id)
        context['customer'] = customer
        return context

class CustomerUpdate(UpdateView):
    form_class = forms.CustomerUpdateForm
    template_name = 'musicstudios/customer_update.html'
    
    def get(self, request, pk):
        order_id = request.session.get('order_id')
        customer = get_object_or_404(Customer, id=pk)
        form = CustomerUpdateForm(instance=customer)
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

class OrderUpdate(UpdateView):
    form_class = forms.OrderUpdateForm
    template_name = 'musicstudios/order_update.html'

    def get(self, request, pk):
        order_id = request.session.get('order_id')
        order = get_object_or_404(Order, id=pk)
        form = OrderUpdateForm(instance=order)
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
            customer_email= order.customer.email,
            line_items=[
                {
                    
                    'price': order.price.stripe_price_id,
                    'quantity': 1,
                },
            ],
            metadata= 
                {
                    'order_id': order.id
                },
            mode='payment',
            success_url=domain + '/musicstudios/success/',
            cancel_url=domain + '/musicstudios/cancel/',
            automatic_tax={'enabled': True},
        )
        print(order_id)
        return redirect(checkout_session.url, code=303)

class SuccessView(TemplateView):
    template_name = "musicstudios/success.html"
    extra_context = sidebar_context
    def get_context_data(self, **kwargs):
        context = super(SuccessView, self).get_context_data(**kwargs)
        order_id = self.request.session.get('order_id')
        order = Order.objects.get(pk=order_id)
        product_id = order.product.id
        product = Product.objects.get(pk=product_id)
        customer = Customer.objects.get(pk=order.customer.id)
        total_paid = self.request.session.get('total_paid')
        print(total_paid)
        context['customer'] = customer
        context['product'] = product
        context['order'] = order
        context['order_total'] = total_paid
        return context
    

class CancelView(TemplateView):
    template_name = "musicstudios/cancel.html"
    extra_context = sidebar_context
    def get_context_data(self, **kwargs):
        context = super(CancelView, self).get_context_data(**kwargs)
        order = self.get_object()
        customer = Customer.objects.get(pk=order.customer.id)
        context['customer'] = customer
        return context