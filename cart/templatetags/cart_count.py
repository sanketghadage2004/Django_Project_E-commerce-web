from django.db.models import Sum,Avg,Min
from django import template
from django.http import request
from cart.models import Cart

register = template.Library()

@register.simple_tag    # decoretors

def cartCount(request):
    # cart count display
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user = request.user).aggregate(cart_sum =Sum('quantity'))
        return carts['cart_sum']

    return 0