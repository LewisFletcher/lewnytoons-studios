from django.db import models
from django.core.validators import MinLengthValidator
from django.db.models import ImageField
from django.db.models import FileField


#Manager Classes

class AlbumVersusSingleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(title='Single')

class SingleVersusAlbumManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(alb='6')


#Data Models

class Album(models.Model):
    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(2, "Must be at least two characters.")]
    )
    release_date = models.DateField()
    picture = models.ImageField(upload_to='albums/', blank=True)
    content_type = models.CharField(max_length=256, blank=True, help_text='The MIMEType of the file')
    description = models.TextField(blank=True)
    objects = models.Manager()
    only_albums = AlbumVersusSingleManager()

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-release_date']


class Song(models.Model):
    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(2, "Must be at least two characters.")]
    )
    release_date = models.DateField(blank=True)
    length = models.CharField(
        max_length=200)
    featured_artists = models.CharField(
        max_length=200,
        blank=True)
    picture = models.ImageField(upload_to='singles/', blank=True)
    content_type = models.CharField(max_length=256, blank=True, help_text='The MIMEType of the file')
    description = models.TextField(blank=True)
    alb = models.ForeignKey(Album, on_delete=models.CASCADE)
    audio_file = models.FileField(upload_to='music_audio/', blank=True)
    objects = models.Manager()
    only_singles = SingleVersusAlbumManager()
    
    def total_songs(self):
        return Song.objects.count()


    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-release_date']
