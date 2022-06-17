from django.db import models
# Create your models here.


class ProductCategory(models.Model):
    """ product category model """
    name = models.CharField(max_length=200)
    status = models.BooleanField(default= True)

    def __str__(self):
        return str(self.name)


class Product(models.Model):
    """ product model """
    product_category = models.ForeignKey(ProductCategory , on_delete= models.CASCADE, related_name="Product")
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8 , decimal_places=2)
    description = models.TextField()
    cover_image = models.ImageField()
    sku = models.CharField(max_length=200)
    status = models.BooleanField(default= True)

    def __str__(self):
        return str(self.name)
    

class Product_images(models.Model):
    """ multiple images model file """
    product = models.ForeignKey(Product, on_delete= models.CASCADE, related_name= 'ProductImages')
    images = models.ImageField()
    status = models.BooleanField(default= True)

    def __str__(self):
        return str(self.product)