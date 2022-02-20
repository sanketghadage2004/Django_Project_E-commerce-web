from email.mime import image
from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    intro = models.TextField()
    body = models.TextField()
    blogimage = models.ImageField()
    author = models.CharField(max_length=20)
    date_added = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return str(self.title)
    
    
    class Meta:
        ordering = ['-date_added']
