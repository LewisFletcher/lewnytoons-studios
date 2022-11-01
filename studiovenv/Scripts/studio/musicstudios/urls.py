from django.urls import path
from . import views
from .views import (
    CreateCheckoutSessionView,
    SuccessView,
    CancelView,
)
urlpatterns = [
    path('', views.StudiosOverview.as_view(), name='musicstudios'),
    path('order-details/', views.orderdetails, name='orderdetails'),
    path('customer-details/', views.CustomerDetails.as_view(), name='custdetails'),
    path('order-details/prices/', views.prices, name='prices'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),
    path('create-checkout-session/<pk>/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
]