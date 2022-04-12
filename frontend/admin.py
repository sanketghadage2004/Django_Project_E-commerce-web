from django.contrib import admin
from .models import Contact


# Register your models here.
class ContactAdmin(admin.ModelAdmin):
    """admin panel customization"""
    list_display = ('name',  'message','email','time')

admin.site.register(Contact,ContactAdmin)