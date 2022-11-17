from django.views.generic.base import View
from django.shortcuts import render
from blog.models import Post
from music.models import Song

 
class HomeView(View):
    def get(self, request):
        blog_photo = Post.objects.order_by('-created_at')[:1]
        single_cover = Song.objects.filter(alb_id=6)[:1]
        context = {
            'blog_photo' : blog_photo,
            'single_cover' : single_cover,
        }
        return render(request, 'home/homepage.html', context)