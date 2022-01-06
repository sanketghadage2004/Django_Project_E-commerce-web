from django.shortcuts import render
from django.http import HttpResponse, request
from django.views import View
from product.models import ProductCategory, Product
# Create your views here.

def home_page(request):
    product_categories = ProductCategory.objects.filter(status=True)
    products = Product.objects.filter(status = True)
    context = {
        'product_categories':product_categories
    }
    
    return render(request, 'home.html', context)


class ProductListingView(View):

    def get(self, request):
        product_categories = ProductCategory.objects.filter(status=True)
        products = Product.objects.filter(status = True)
        context = {
        'product_categories':product_categories,
        'products': products
        }
        
        return render(request, 'product_listing.html', context) 