from django.urls import path
from . import views


urlpatterns = [
    path('', views.MerchView.as_view(), name='merch'),
]