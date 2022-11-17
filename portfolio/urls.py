from django.urls import path
from . import views


urlpatterns = [
    path('', views.PortfolioView.as_view(), name='portfolio'),
]