from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name= "UserProfiles")
    mobile = models.IntegerField(null=True , blank= True )
    address = models.TextField(null=True , blank= True )
    profile_picture = models.ImageField(null = True, blank = True)


    def __str__(self):
        return str(self.user)

