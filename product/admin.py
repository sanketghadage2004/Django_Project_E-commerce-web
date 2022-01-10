from django.contrib import admin, messages
from django.contrib.admin.decorators import action, display
from django.db.models.base import Model
from product.models import ProductCategory, Product, Product_images
from order.models import Reviews

# Register your models files here.
   
def ActiveStatus(modeladmin, request, queryset):
    queryset.update(status = True)
    messages.success(request, ('This record(s) marked as Active Status successfully !'))

def InActiveStatus(modeladmin, request, queryset):
    queryset.update(status = False)
    messages.error(request, 'This record(s) marked as InActive Status successfully !')

# here is a  admin panel customization 

class ProductCategoryAdmin(admin.ModelAdmin):
    """admin panel customization"""
    list_display = ('name',  'status',)
    list_filter = ('status',)
    actions = (ActiveStatus, InActiveStatus)

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
    list_filter = ('product_category','status',)
    search_fields = ('name','price','sku',)
    actions = (ActiveStatus, InActiveStatus)

admin.site.register(Product,ProductAdmin)


# admin.site.register(Product_images)