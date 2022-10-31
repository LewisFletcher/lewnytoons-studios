from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings
import datetime
from django.utils import timezone
from django.db.models import ImageField

#Blog Managers



# Blog Models

class Category(models.Model):
    name = models.CharField(
        max_length=30,
        validators=[MinLengthValidator(3, "Category type must be at least 3 characters.")]
    )
    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(5, "Title must be at least 5 characters.")]
        )
    blog_textbox1 = models.TextField(help_text='Displayed in the preview.')
    blog_textbox2 = models.TextField(help_text='Displayed after the first textbox on the detail page.')
    blog_textbox3 = models.TextField(help_text='Displayed after the second image on the detail page.')
    blog_photo1 = models.ImageField(upload_to='blog_photos/', blank=True, help_text='Displayed in the preview and the top of the blog post.')
    blog_photo2 = models.ImageField(upload_to='blog_photos/', blank=True, help_text='Displayed before the final textbox, after the second textbox.')
    blog_photo1_ex = models.TextField(blank=True, help_text='Information displayed below the picture. Optional.')
    blog_photo2_ex = models.TextField(blank=True, help_text='Information displayed below the picture. Optional.')
    summary = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(20, "Displayed in the preview and top of the article.")]
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_posts(self):
        return Post.objects.count()

    def __str__(self):
        return self.title
    def recent_posts(self):
        return self.created_at >= timezone.now() - datetime.timedelta(days=30)

    class Meta:
        ordering = ['-created_at']