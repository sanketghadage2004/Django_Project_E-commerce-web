from django.shortcuts import render
from django.views import View
from product.models import ProductCategory, Product
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import request, HttpResponse
from cart.views import Cart
from.models import Contact
from django.contrib import messages



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

        return render(request, 'product-details.html', context )





def contact(request):
    product_categories = ProductCategory.objects.filter(status=True)
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        message=request.POST['message']

        if len(name)<2 or len(email)<5 or len(message)<5:
            messages.error(request, 'Please fill form correctly...')
        else:
            contact=Contact(name=name,email=email, message=message)
            contact.save()
            messages.success(request, 'Message Send Successfully...')


    return render(request, 'contact.html',{ 'product_categories':product_categories} )


def profile(request):
    """user profile View"""
    
    product_categories = ProductCategory.objects.filter(status=True)

    return render(request,'userprofile.html',{ 'product_categories':product_categories})


def orderDetails(request):
        """order details View"""
    
        product_categories = ProductCategory.objects.filter(status=True)
        cartProducts = Cart.objects.filter(user=request.user)

        carts = {}
        subTotal = 0
        total = 0
        shippingCost = 50
        for key, cartProduct in enumerate(cartProducts):
            productTotal = int(cartProduct.quantity) * int(cartProduct.Product.price)
            total += productTotal
            subTotal += productTotal
            carts[key] = {
                'product_image': cartProduct.Product.cover_image,
                'product_name': cartProduct.Product.name,
                'product_price': cartProduct.Product.price,
                'quantity': cartProduct.quantity,
                'productTotal': productTotal,
                'cart_id':cartProduct.id
            }
        
        
        total = shippingCost + subTotal
        carts = list(carts.values())

        context = {
            'product_categories': product_categories,
            'cartProducts': carts,
            'subTotal':subTotal,
            'shippingCost': shippingCost,
            'total':total,
        }
        return render(request,'order.html',context)






"""dummy user """
# def test_login(request):
#     user = User.objects.get(id = 2)
#     login(request, user)
