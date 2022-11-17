from django.shortcuts import render
from django.views.generic.base import View

# Create your views here.

class PortfolioView(View):
    def get(self, request):
        context = {
            'sidebarhead' : 'Quick Find',
            'sidebar1' : 'Lewis Fletcher - About',
            'sidebar2' : 'Site Background',
            'sidebar3' : 'My Skills',
            'sidebar4' : 'Roles I\'m Looking For',
            'sidebar5' : 'My Projects',
            'sidebar6' : 'Contact Info',
            'sb1url' : '#lewisabout',
            'sb2url' : '#background',
            'sb3url' : '#skills',
            'sb4url' : '#roles',
            'sb5url' : '#projects',
            'sb6url' : '#lewiscontact',
        } 
        return render(request, 'portfolio/about.html', context)