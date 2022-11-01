from django.views.generic.base import View
from django.shortcuts import render, redirect, HttpResponse
import stripe
from django.conf import settings
from django.http import JsonResponse
from .models import Price, Product, Order, Customer
from . import forms
from .forms import OrderForm
from django.views.generic import TemplateView, CreateView


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
    return HttpResponse(form['prices'])

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
    

class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        price = Price.objects.get(id=self.kwargs["pk"])
        YOUR_DOMAIN = "http://127.0.0.1:8000"  # change in production
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': price.stripe_price_id,
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
        return redirect(checkout_session.url)

class SuccessView(TemplateView):
    template_name = "success.html"

class CancelView(TemplateView):
    template_name = "cancel.html"