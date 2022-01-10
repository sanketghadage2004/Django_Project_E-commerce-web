from django.contrib import admin
from django.db import models
from django.db.models.base import Model
from . models import Order, Order_Details , Reviews 
# Register your models here.



class OrderDetailAdmin(admin.StackedInline):
    model = Order_Details
    classes = ('collapse',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user','date', 'order_status', 'payment_status')
    inlines = (OrderDetailAdmin,)
    list_filter = ('order_status', 'payment_status',)
    date_hierarchy = 'date'

admin.site.register(Order, OrderAdmin)

# admin.site.register(Order_Details)







# admin.site.register(Reviews)
# admin.site.register(Payment)