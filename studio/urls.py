from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings
import os
from django.conf.urls.static import static
from musicstudios.views import stripe_webhook

urlpatterns = [
    path('lewnyupdate/', admin.site.urls),
    #path("__reload__/", include("django_browser_reload.urls")),
    #path('__debug__/', include('debug_toolbar.urls')),
    path('', include('home.urls')),
    path('portfolio/', include('portfolio.urls')),
    path('blog/', include('blog.urls')),
    path('music/', include('music.urls')),
    path('merch/', include('merch.urls')),
    path('musicstudios/', include('musicstudios.urls')),
    path('webhooks/stripe/', stripe_webhook, name='stripe-webhook'),
    
]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('favicon.ico', serve, {
            'path': 'favicon.ico',
            'document_root': os.path.join(BASE_DIR, 'static/favicon_io'),
        }
    ),
]
