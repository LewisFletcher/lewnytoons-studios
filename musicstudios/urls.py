from django.urls import path
from . import views
from .views import (
    SuccessView,
    CancelView,
    CreateCheckoutSessionView
)

#Still Need: Refund Policy (could be in FAQ's), Order Number Function for model, Tutor Session Portal

urlpatterns = [
    path('', views.StudiosOverview.as_view(), name='musicstudios'),
    path('frequently-asked-questions/', views.FrequentQuestion.as_view(), name='faq'),
    path('before-after/', views.BeforeAfter.as_view(), name='before_after'),
    path('order-details/', views.orderdetails, name='orderdetails'),
    path('customer-details/', views.CustomerDetails.as_view(), name='custdetails'),
    path('existing-customer/', views.CustomerSelect.as_view(), name='already_cust'),
    path('begin-order/', views.begin_order, name='begin_order'),
    path('customer-details/upload', views.custupload, name='custupload'),
    path('order-details/prices/', views.prices, name='prices'),
    path('order-details/upload', views.orderupload, name='orderupload'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),
    path('order-review/<int:pk>', views.OrderReview.as_view(), name='order-review'),
    path('customer-details/<int:pk>/update', views.CustomerUpdate.as_view(), name='custupdate'),
    path('order-details/<int:pk>/update', views.OrderUpdate.as_view(), name='orderupdate'),
    path('delete/', views.orderdelete, name='orderdelete'),
    path('create-checkout-session/<int:pk>', CreateCheckoutSessionView.as_view(), name='create-checkout-session')
]