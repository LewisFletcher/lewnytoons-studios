from django.contrib import admin
from .models import Post, Category

# Blog Models Registry

admin.site.register(Post)
admin.site.register(Category)