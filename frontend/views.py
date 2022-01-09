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
    context = {
        'product_categories':product_categories,
        'latestProductCategories':latestProductCategories
    }
    
    return render(request, 'home.html', context)


class ProductListingView(View):

    def get(self, request, product_category_id= None):
        product_categories = ProductCategory.objects.filter(status=True)
        products = Product.objects.filter(status = True, product_category_id = product_category_id)
        context = {
        'product_categories':product_categories,
        'products': products
        }
        
        return render(request, 'product_listing.html', context) 


class ProductDetailsView(View):
    
    def get(self, request, product_id=None):
        product_categories = ProductCategory.objects.filter(status=True)
        productDetail = Product.objects.get(id=product_id) 
        relatedProducts = Product.objects.filter(status = True, product_category_id = productDetail.product_category_id).exclude(id= product_id)
        context = {
            'product_categories':product_categories,
            'productDetail': productDetail,
            'relatedProducts':relatedProducts
        }
        return render(request, 'product-details.html', context )