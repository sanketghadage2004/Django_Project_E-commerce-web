from django.shortcuts import render
from django.views import View
from product.models import ProductCategory, Product
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import request, HttpResponse


# Create your views here.

def home_page(request):
    # showing product category
    product_categories = ProductCategory.objects.filter(status=True)
    # showing product on home page category wise
    latestProductCategories = ProductCategory.objects.filter(status=True).order_by('-id')[0:5]
    context = {
        'product_categories':product_categories,
        'latestProductCategories':latestProductCategories,
        
    }
    
    return render(request, 'home.html', context)


class ProductListingView(View):

    def get(self, request, product_category_id= None):
        product_categories = ProductCategory.objects.filter(status=True)
        search = request.GET.get('search')
        sorting = request.GET.get('sorting')
        print(request.GET)
        minPrice=request.GET.get('min')
        maxPrice=request.GET.get('max')

        
        searchDict = {
            'status' : True,
            }


        if minPrice:
            minPrice= int(minPrice.replace('$',''))
            searchDict['price__gte'] = minPrice

        if maxPrice:
            maxPrice= int(maxPrice.replace('$',''))
            searchDict['price__lte'] = maxPrice
        
        # print(minPrice)

        if product_category_id and product_category_id != 'None':
            searchDict['product_category_id'] = product_category_id
        if search:
            searchDict['name__contains']=search
        if sorting =='low':
            products = Product.objects.filter(**searchDict).order_by('price')
        elif sorting =='high':
            products = Product.objects.filter(**searchDict).order_by('-price')
        else:
            products = Product.objects.filter(**searchDict)
        context = {
        'product_categories':product_categories,
        'products': products,
        'product_category_id':product_category_id,
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

        # user = User.objects.get(id)
        return render(request, 'product-details.html', context )





def contact(request):

    product_categories = ProductCategory.objects.filter(status=True)


    return render(request, 'contact.html',{ 'product_categories':product_categories} )

# class Contact(View):

#     def post(self):
#         return render(request, 'home_page')


# def test_login(request):
#     user = User.objects.get(id = 2)
#     login(request, user)
