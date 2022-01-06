from django.contrib import admin
from product.models import ProductCategory, Product, Product_images

# Register your models files here.
   
# here is a  admin panel customization 

admin.site.register(ProductCategory)

admin.site.register(Product)

admin.site.register(Product_images)