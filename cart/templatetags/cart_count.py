from django.db.models import Sum,Avg,Min
from django import template
from django.http import request
from cart.models import Cart

register = template.Library()

@register.simple_tag # decoretors

def cartCount(request):
    carts = Cart.objects.filter(user = request.user).aggregate(cart_sum =Sum('quantity'))
    # print(cartCount ,['cart_sum'])
    # print(carts)
    return carts['cart_sum']