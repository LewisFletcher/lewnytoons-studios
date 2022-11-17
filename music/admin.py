from django.contrib import admin
from .models import Song, Album

# Register your models here.

class MusicAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Song, MusicAdmin)
admin.site.register(Album, MusicAdmin)