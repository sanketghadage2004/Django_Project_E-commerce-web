from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from . models import Cart
# Create your views here.


def addToCart(request):
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity'))

    try:
        checkCart = Cart.objects.get(user=request.user, Product_id=product_id )
        checkCart.quantity = checkCart.quantity +quantity
        checkCart.save()
    
    except: Cart.DoesNotExist

    Cart.objects.create(
        user = request.user,
        Product_id= product_id,
        quantity=quantity,

    )

    return redirect('ProductDetailsView',product_id=product_id)
    