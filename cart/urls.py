from django.urls import path
from . import views

urlpatterns = [
    path('add-to-cart', views.addToCart, name='addToCart'),
    path('my-cart', views.MyCart.as_view(), name='MyCart'),
]
