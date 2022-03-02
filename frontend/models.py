import email
from email import message
from unicodedata import name
from xmlrpc.client import DateTime
from django.db import models

# Create your models here.

class Contact(models.Model):
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    message=models.TextField()
    time=models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return str(self.name)

