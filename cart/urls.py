from django.urls import path
from . import views

urlpatterns = [
    path('add-to-cart', views.addToCart, name='addToCart'),
    path('my-cart', views.MyCart.as_view(), name='MyCart'),
    path('checkout', views.Checkout.as_view(), name='Checkout'),
    # path('capture-payment', views.CapturePayment.as_view(), name='CapturePayment'),
    path('payment-success', views.PaymentSuccess.as_view(), name='PaymentSuccess'),
    path('webhook', views.RazorpayWebhook),
    path('thank-you', views.ThankYou, name='ThankYou'),
    path('order-status', views.orderStatus, name='orderStatus')
]
