from django.contrib import admin
from django.contrib.admin.decorators import display
from django.db.models.base import Model
from product.models import ProductCategory, Product, Product_images
from order.models import Reviews

# Register your models files here.
   
# here is a  admin panel customization 

class ProductCategoryAdmin(admin.ModelAdmin):
    """admin panel customization"""
    list_display = ('name',  'status',)

admin.site.register(ProductCategory, ProductCategoryAdmin)


# class ProductImageAdmin(admin.StackedInline):
#     model = Product_images
    
class ProductImageAdmin(admin.TabularInline):
    model = Product_images
    classes = ('collapse',)

class ProductReviewAdmin(admin.TabularInline):
    model = Reviews
    classes = ('collapse',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'sku', 'product_category','status')
    inlines = (ProductImageAdmin, ProductReviewAdmin,)

admin.site.register(Product,ProductAdmin)


# admin.site.register(Product_images)