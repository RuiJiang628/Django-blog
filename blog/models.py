from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone, html
from django.utils.html import strip_tags
import markdown

# each post belongs to a category, and each category can have multiple posts
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
# each post can have multiple tags, and each tag can have multiple posts
class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
# post: title, body, created_time, modified_time, excerpt (allowed to be empty), category, tags, author
class Post(models.Model):
    title = models.CharField(max_length=70)
    body = models.TextField()
    created_time = models.DateTimeField(default=timezone.now)
    modified_time = models.DateTimeField()
    excerpt = models.CharField(max_length=200, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    views = models.PositiveIntegerField(default = 0, editable = False)

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_time']

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()
        if not self.excerpt:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            self.excerpt = strip_tags(md.convert(self.body))[:54]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})
    
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])