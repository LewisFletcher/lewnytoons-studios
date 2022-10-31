from .models import Order, Customer
from django import forms
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class OrderForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

    class Meta:
        model = Order
        fields = ['product', 'price', 'cust_requests', 'reference_track', 'music_file']


class CustomerForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'phone', 'email']
