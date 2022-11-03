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
from django.views.generic import TemplateView, CreateView, DetailView


sidebar_context = {
    'sidebarhead' : 'Quick Find',
    'sidebar1' : 'LewnyToons - About',
    'sidebar2' : 'Services Offered',
    'sidebar3' : 'Mixing & Mastering',
    'sidebar4' : 'Mastering Only',
    'sidebar5' : 'Request a Feature',
    'sidebar6' : 'Request a Tutor',
    'sb1url' : '/music#about',
    'sb2url' : '#services',
    'sb3url' : '#mnmpack',
    'sb4url' : '#mpack',
    'sb5url' : '#feature',
    'sb6url' : '#tutor',
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
        print(request.session['customer_id'])
        if form.is_valid():
            customer = form.save()
            request.session['customer_id'] = customer.id
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

class StudiosOverview(View):
    def get_context_data(self, **kwargs):
        product = Product.objects.all()
        prices = Price.objects.all()
        context = super(StudiosOverview, self).get_context_data(**kwargs)
        context.update({
            "product": product,
            "prices": prices
        })
        return context
    
    def get(self, request):
        context = {
            'page_headline' : 'Studio Services'
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




class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        product_id = self.kwargs["pk"]
        product = Product.objects.get(id=product_id)
        domain = "https://lewnytoonsstudios.com"
        if settings.DEBUG:
            domain = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': product.prices.stripe_price_id,
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=domain + '/success.html',
            cancel_url=domain + '/cancel.html',
            automatic_tax={'enabled': True},
        )
        return JsonResponse({
            'id' : checkout_session.id
        })

class SuccessView(TemplateView):
    template_name = "success.html"

class CancelView(TemplateView):
    template_name = "cancel.html"