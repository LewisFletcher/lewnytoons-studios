from django.urls import path
from . import views
from .views import (
    SuccessView,
    CancelView,
    CreateCheckoutSessionView
)
urlpatterns = [
    path('', views.StudiosOverview.as_view(), name='musicstudios'),
    path('order-details/', views.orderdetails, name='orderdetails'),
    path('customer-details/', views.CustomerDetails.as_view(), name='custdetails'),
    path('customer-details/upload', views.custupload, name='custupload'),
    path('order-details/prices/', views.prices, name='prices'),
    path('order-details/upload', views.orderupload, name='orderupload'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),
    path('create-checkout-session/<int:pk>', CreateCheckoutSessionView.as_view(), name='create-checkout-session')
]