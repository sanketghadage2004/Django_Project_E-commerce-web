from django.db import models
from django.contrib.auth.models import User
from product.models import Product

# Create your models here.


class Cart(models.Model):
    """user cart model files """
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    Product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        """string representetion of cart"""
        return f'USER: {self.user} / PRODUCT: {self.Product} / QUANTITY: {self.quantity}'
