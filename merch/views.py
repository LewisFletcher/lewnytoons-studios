from django.shortcuts import render
from django.views.generic.base import View

# Create your views here.

class MerchView(View):
    def get(self, request):
        return render(request, 'merch/shop.html')