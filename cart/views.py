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

        return render(request, self.template_name, context)


    def post(self, request):
        cartsIds = request.POST.getlist('card_id')
        quantities  = request.POST.getlist('quantity')
        
        for cartKey , cartsId in enumerate(cartsIds):
            try:
                cartObject = Cart.objects.get(id = cartsId)
                if quantities[cartKey]== 0:
                    cartObject.delete() 
                else:
                    cartObject.quantity = quantities[cartKey]
            except Cart.DoesNotExist:
                pass

        return redirect('MyCart')


class Checkout(View):
    template_name = 'checkout.html'
    def get(self, request):
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
                
                'product_name': cartProduct.Product.name,
                'productTotal': productTotal,
                
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


        return render(request, self.template_name, context)
    