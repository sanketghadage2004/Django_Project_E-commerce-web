from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.generic.base import View

import cart
from . models import Cart
from django.views import View
from product.models import ProductCategory, Product

# Create your views here.


def addToCart(request):
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity'))

    cart, flag = Cart.objects.get_or_create(user=request.user, Product_id=product_id )
    if flag:
        cart.quantity = quantity
    else:    
        cart.quantity = quantity + cart.quantity
    cart.save()

    return redirect('ProductDetailsView',product_id=product_id)

class MyCart(View):
    
    template_name = 'my-cart.html'

    def get(self,request):
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
                'productTotal': productTotal
            }
        
        
        total = shippingCost + subTotal
        carts = list(carts.values())

        context = {
            'productCategories': product_categories,
            'cartProducts': carts,
            'subTotal':subTotal,
            'shippingCost': shippingCost,
            'total':total,
        }

        return render(request, self.template_name, context)