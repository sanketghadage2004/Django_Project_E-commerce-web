from django.db import models
from django.contrib.auth.models import User
from product.models import Product
from datetime import datetime

# models file here ->.

class Order(models.Model):
    """order model class """
    ORDER_STATUS = (
        ('Pending', 'Pending'),
        ('In-progress', 'In-progress'),
        ('Delivered', 'Delivered'),
        ('Canceled', 'Canceled')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now())
    user_name = models.CharField(max_length=200)
    user_address = models.TextField()
    status = models.CharField(choices=ORDER_STATUS, max_length=255, default='pending')
    payment_status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id} {self.order_status}'


class Order_Details(models.Model):
    """ order detail model """
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=8 , decimal_places=2)

    def __str__(self):
        return f'{self.order.id} {self.product}'


class Reviews(models.Model):
    """reviews model """
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    product =  models.ForeignKey(Product, on_delete=models.CASCADE)
    reviews = models.TextField()
    date = models.DateTimeField(default=datetime.now())
    status = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user} {self.product} {self.date}'


class Payment(models.Model):
    """payment model files"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=255)
    payment_id  = models.CharField(max_length=255)
    payment_status  = models.CharField(max_length=255)
    payment_method  = models.CharField(max_length=255)

    def __str__(self):
        return str(self.transaction_id)