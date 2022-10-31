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
            'sb2url' : '#',
            'sb4url' : '/portfolio',
            'sb5url' : '/',
            'sb6url' : '#',
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
        strval =  request.GET.get("search", False)
        template = 'blog/all_posts.html'
        max_value = Post.total_posts(self)
        ran_num = str(random.randint(1, max_value))
        if strval :
            query = Q(title__icontains=strval)
            query.add(Q(blog_textbox1__icontains=strval), Q.OR)
            query.add(Q(blog_textbox2__icontains=strval), Q.OR)    
            query.add(Q(blog_textbox3__icontains=strval), Q.OR)
            query.add(Q(summary__icontains=strval), Q.OR)
            post_list = Post.objects.filter(query).distinct().select_related()
        else :
            post_list = Post.objects.all()

        context = {
            'post_list' : post_list,
            'page_headline' : 'All Posts',
            'search' : strval,
            'category_list' : category_list,
            'page_obj' : page_obj,
            'sb3url' : (ran_num),
        }
        context.update(sidebar_context)
        return render(request, template, context)

class BlogDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    extra_context = sidebar_context

class CategoryView(DetailView, MultipleObjectMixin):
    paginate_by = 2
    model = Category
    template_name = 'blog/category_view.html'
    extra_context = sidebar_context

    def get_context_data(self, **kwargs):
        category_list = Category.objects.all()
        object_list = Post.objects.filter(category = self.get_object())       
        context = super(CategoryView, self).get_context_data(object_list=object_list,**kwargs, category_list=category_list)   
        return context
    
    #def get_queryset(self):
        #return Post.objects.filter(category_id=self.kwargs['pk']).order_by('-created_at')