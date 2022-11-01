from .models import Order, Customer, Product, Price
from django import forms
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from dynamic_forms import DynamicField, DynamicFormMixin

class OrderForm(DynamicFormMixin, forms.Form):

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
    
    def price_choices(form):
        product = form['product'].value()
        return Price.objects.filter(product=product)

    def initial_price(form):
        product = form['product'].value()
        return Price.objects.filter(product=product).first()
    
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        initial=None,
        label= "Select a Product:",
        widget= forms.RadioSelect(
            attrs={
                'hx-get' : 'prices',
                'hx-target' : '#prices',
                'hx-swap' : 'innerHTML'
            }),
        required=True,

    )

    prices = DynamicField(
        forms.ModelChoiceField,
        queryset=price_choices,
        initial=initial_price,
        label= "Select a price:"
    )

    cust_requests = forms.CharField(
        label = 'Enter any specific requests here: (Leave blank if none): ',
        required=False
    )

    reference_track = forms.FileField(
        label = 'Upload a reference track, if applicable.',
        required=False
    )

    music_file = forms.FileField(
        label = 'Upload your project here. Please ensure project has been zipped prior to uploading.',
        required=True
    )

class CustomerForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'phone', 'email']
