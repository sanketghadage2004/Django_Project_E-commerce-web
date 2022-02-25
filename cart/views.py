from multiprocessing import context
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import json
from . models import Cart
from django.views import View
from product.models import ProductCategory
import razorpay
from datetime import datetime
from order.models import Order, Payment, Order_Details
from django.views.decorators.csrf import csrf_exempt



# Create your views here.

@login_required

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


@method_decorator(login_required, name='dispatch')
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

@method_decorator(login_required, name='dispatch')
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
        cartData = list(carts.values())

        context = {
            'product_categories': product_categories,
            'carts': cartData,
            'subTotal':subTotal,
            'shippingCost': shippingCost,
            'total':total,
        }


        return render(request, self.template_name, context)


    def post(self, request):

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')

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
                'first_name' : first_name,
                'last_name' : last_name,
                'address' : address,
            }
        return render(request, 'capture-payment.html', context)


class PaymentSuccess(View):
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
        
        return JsonResponse({'status':'success'})


@csrf_exempt
def RazorpayWebhook(request):
    requestBody = json.load(request.body.decode('utf-8'))
    payload = requestBody['payload']
    if payload['payment']:
        order_id = payload['payment']['entity']['order_id']
        try:
            order = Order.objects.get(razor_pay_order_id=order_id)
            payment = Payment.objects.get_or_create(order=order)
            payment.payment_id=payload['payment']['entity']['id']
            payment.payment_status=payload['payment']['entity']['status']
            payment.payment_method=payload['payment']['entity']['method']
            payment.created_at=payload['payment']['entity']['created_at']
            payment.amount=payload['payment']['entity']['amount']
            payment.save()
            order.payment_status=True
            order.save()
            return JsonResponse({'status':'success'})
        except:
            return JsonResponse({'status':'failed'})


def ThankYou(request):
    product_categories = ProductCategory.objects.filter(status=True)
    context={
        'product_categories': product_categories,
    }
    return render(request, 'thank-you.html',context)


def orderStatus(request):
    product_categories = ProductCategory.objects.filter(status=True)
    context={
        'product_categories': product_categories,
    }
    return render(request, 'order-status.html',context)