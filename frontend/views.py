from django.shortcuts import render
from django.http import HttpResponse, request
from django.views import View
from product.models import ProductCategory, Product
# Create your views here.

def home_page(request):
    # showing product category
    product_categories = ProductCategory.objects.filter(status=True)

    # showing product on home page category wise
    latestProductCategories = ProductCategory.objects.filter(status=True).order_by('-id')[0:5]
    # products = Product.objects.filter(status = True)
    context = {
        'product_categories':product_categories,
        'latestProductCategories':latestProductCategories
        # 'products':products
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