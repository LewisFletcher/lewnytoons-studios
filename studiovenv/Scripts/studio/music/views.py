from urllib.request import url2pathname
from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic import ListView, DetailView
from .models import Album, Song
import random
from django.utils.html import mark_safe
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


#sibebar contexts

sidebar_context = {
    'sidebarhead' : 'Quick Find',
    'sidebar1' : 'LewnyToons - About',
    'sidebar2' : 'Albums',
    'sidebar3' : 'Singles',
    'sidebar4' : 'I\'m Feeling Lucky',
    'sidebar5' : 'Mixing/Mastering Services',
    'sidebar6' : 'Contact Info',
    'sb1url' : '/music#about',
    'sb2url' : '/music#albums',
    'sb3url' : '/music#singles',
    
    'sb5url' : '/musicstudios',
    'sb6url' : '/musicstudios#contact',
}

#Views

class MusicView(ListView):
    model = Album, Song
    def get(self, request):
        album_list = Album.only_albums.all()
        single_list = Song.only_singles.all()
        max_value = Song.total_songs(self)
        ran_num = str(random.randint(1, max_value))
        context = {
            'album_list' : album_list,
            'single_list' : single_list,
            'sb4url' : ('/music/' + ran_num + '/play'),
        }
        context.update(sidebar_context)
        return render(request, 'music/all_music.html', context)

class AlbumDetailView(DetailView):
    model = Album
    template_name = 'music/album_detail.html'
    extra_context = sidebar_context
    max_value = Song.total_songs(self=Song)
    ran_num = str(random.randint(1, max_value))
    sb4_url = ('/music/' + ran_num + '/play')
    extra_context.update({'sb4url' : sb4_url})   
    def get_context_data(self, **kwargs):
        context = super(AlbumDetailView, self).get_context_data(**kwargs)
        album = self.get_object()
        context['album_songs'] = album.song_set.all()
        return context
    

class PlaySongView(DetailView):
    model = Song
    template_name = 'music/play_song.html'
    extra_context = sidebar_context
    max_value = Song.total_songs(self=Song)
    ran_num = str(random.randint(1, max_value))
    sb4_url = ('/music/' + ran_num + '/play')
    extra_context.update({'sb4url' : sb4_url})   
    def get_context_data(self, **kwargs):
        context = super(PlaySongView, self).get_context_data(**kwargs)
        song = self.get_object()
        context['album'] = song.alb
        return context

class AlbumRandomSongView(AlbumDetailView):
    def redirect_to_play(request):
        max_value = Song.total_songs(self=Song)
        ran_num = str(random.randint(1, max_value))
        return HttpResponseRedirect(reverse('the_music:random_song', kwargs=(ran_num,)))
