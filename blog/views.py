from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Category, Post
from django.db.models import Q
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.core.paginator import Paginator
from django.views.generic.list import MultipleObjectMixin
import random

#Sidebar Context

sidebar_context = {
            'sidebarhead' : 'Quick Find',
            'sidebar1' : 'All Posts',
            'sidebar2' : 'Most Recent',
            'sidebar3' : 'I\'m Feeling Lucky',
            'sidebar4' : 'Lewis Fletcher - About',
            'sidebar5' : 'LewnyToons Studios Home',
            'sidebar6' : 'Contact',
            'sb1url' : '/blog',
            'sb4url' : '/portfolio',
            'sb5url' : '/',
            'sb6url' : '/portfolio#lewiscontact',
}

#Views

class BlogView(ListView):
    model = Post
    def get(self, request):
        post_list = Post.objects.all()
        paginator = Paginator(post_list, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        category_list = Category.objects.all()
        template = 'blog/all_posts.html'
        try:
            max_value = 5
            ran_num = str(random.randint(1, max_value))
            recent = Post.most_recent(self)
        except:
            max_value = '1'
            ran_num = '1'
            recent = '#'
        context = {
            'post_list' : post_list,
            'page_headline' : 'All Posts',
            'category_list' : category_list,
            'page_obj' : page_obj,
            'sb2url' : (recent),
            'sb3url' : (ran_num),
        }
        context.update(sidebar_context)
        return render(request, template, context)

class BlogDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    extra_context = sidebar_context
    max_value = 5
    ran_num = str(random.randint(1, max_value))
    recent = '1'
    recent_url = ('/blog/' + recent)
    ran_num_url = ('/blog/' + ran_num)
    context = {
            'sb2url' : (recent_url),
            'sb3url' : (ran_num_url),
    }
    extra_context.update(context)

class CategoryView(DetailView, MultipleObjectMixin):
    paginate_by = 2
    model = Category
    template_name = 'blog/category_view.html'
    extra_context = sidebar_context
    max_value = 5
    ran_num = str(random.randint(1, max_value))
    recent = '1'
    recent_url = ('/blog/' + recent)
    ran_num_url = ('/blog/' + ran_num)
    context = {
            'sb2url' : (recent_url),
            'sb3url' : (ran_num_url),
    }
    extra_context.update(context)
    def get_context_data(self, **kwargs):
        category_list = Category.objects.all()
        object_list = Post.objects.filter(category = self.get_object())       
        context = super(CategoryView, self).get_context_data(object_list=object_list,**kwargs, category_list=category_list)   
        return context