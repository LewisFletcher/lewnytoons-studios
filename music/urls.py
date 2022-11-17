from django.urls import path
from . import views

app_name = 'the_music'

urlpatterns = [
    path('', views.MusicView.as_view(), name='music'),
    path('<int:pk>/', views.AlbumDetailView.as_view(), name='album_detail'),
    path('<int:pk>/play', views.PlaySongView.as_view(), name='play'),
    path('<int:pk>/random', views.AlbumRandomSongView.as_view(), name='random_song')
]