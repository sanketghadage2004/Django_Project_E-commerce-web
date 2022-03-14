from itertools import product
from django.http import Http404
from django.shortcuts import render
from rest_framework import viewsets, filters, views, response,authentication, status
from rest_framework.permissions import IsAuthenticated

from order.models import Order, Order_Details
from . import serializers, permissions
from product.models import Product, ProductCategory
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from cart.models import Cart
import razorpay
from datetime import datetime
from django.contrib.auth.models import User


class UserAuthApi(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ProductCategoryView(viewsets.ModelViewSet):
    """Product-categories API"""
    http_method_names = ['get']
    serializer_class=serializers.ProductCategorySerializer
    queryset=ProductCategory.objects.all()


class ProductView(viewsets.ModelViewSet):
    """Product API"""
    http_method_names = ['get']
    serializer_class=serializers.ProductSerializer
    queryset=Product.objects.all()
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields=('product_category__id','name')
    ordering_fields=('price',)


class CartsView(views.APIView):
    """ Cart API """
    authentication_classes = (authentication.TokenAuthentication,)
    permissions_classes = (IsAuthenticated)
    serializer_class = serializers.CartSerializers
    
    def get(self,request):
        queryset = Cart.objects.filter(user = request.user)
        serializer = self.serializer_class(queryset,many=True)
        return response.Response(serializer.data)
    
    def post(self,request):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            quantity = serializer.validated_data.get('quantity')
            product = serializer.validated_data.get('product')
            cart, _ = Cart.objects.get_or_create(product=product, user=request.user)
            cart.quantity = quantity
            if int(quantity) == 0:
                cart.delete()
            else:
                cart.save()
            return response.Response({'status':'success',})
        else:
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, cartId=None):
        if cartId:
            try:
                Cart.objects.get(id=cartId).delete()
                return response.Response({'status' : 'success'})
            except Cart.DoesNotExist:
                return response.Response({'details' : 'No found.'}, status=status.HTTP_404_NOT_FOUND)
        return response.Response({'details' : 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)

    
class Checkout(views.APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permissions_classes = (IsAuthenticated)
    def get (self, request):
        try:
            cartProducts = Cart.objects.filter(user=request.user)
            subTotal = 0
            total = 0
            shippingCost = 50
            for key, cartProduct in enumerate(cartProducts):
                productTotal = int(cartProduct.quantity) * int(cartProduct.Product.price)
                total += productTotal
                subTotal += productTotal
            total = (shippingCost + subTotal ) * 100

            client = razorpay.Client(auth=("rzp_test_M5Cd3ntaZvvW5O", "OiAZK68k1aGB6H7PQOKQmxXx"))
            receipt = f'order_rcptid{request.user.id}'
            data = { "amount": total, "currency": "INR", "receipt":receipt }
            payment = client.order.create(data=data)
            
            if payment.get('id'):
                context = {
                    'order_id': payment['id'],
                    'amount': payment['amount'],
                }
                return response.Response({'status':'success', 'data':context})
            else:
                return response.Response({'details':'Something went wrong !!'}, status=status.HTTP_400_BAD_REQUEST) 
        except Exception as e:
            return response.Response({'details':str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        razorpay_payment_id  = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        cartProducts = Cart.objects.filter(user=request.user)

        if cartProducts:
            order = Order.objects.create(
                user = request.user,
                name=f'{first_name} {last_name}',
                address = address,
                razor_pay_order_id=razorpay_order_id,
                date_time=datetime.now()

            )
            for cartProduct in cartProducts:
                Order_Details.objects.create(
                    order=order,
                    product=cartProduct.product,
                    quantity=cartProduct.quantity,
                    price=cartProduct.product.price,
                )
            cartProducts.delete()
        
        return response.Response({'status':'success'})

class UserView(viewsets.ModelViewSet):
    serializer_class = serializers.UsersSerializer
    queryset = User.objects.filter(is_superuser=False, is_staff=False)