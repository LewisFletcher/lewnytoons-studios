from django.urls import path
from . import views

app_name = 'the_blog'

urlpatterns = [
    path('', views.BlogView.as_view(), name='blog'),
    path('<int:pk>/', views.BlogDetailView.as_view(), name='detail'),
    path('<int:pk>/category',views.CategoryView.as_view(), name='category'),
]