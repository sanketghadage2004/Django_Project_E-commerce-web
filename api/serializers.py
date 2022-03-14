from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from django.contrib.auth.models import User
from product.models import Product, ProductCategory
from cart.models import Cart

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductCategory
        fields = ['id','name']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields = ['id','product_category','name','price','description','cover_image','sku']
        depth = 1

class CartSerializers(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id','Product','quantity',]


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            
            'id','username','first_name','last_name','password','email'
        ]
        extra_kwargs = {
            'password' : {'write_only':True}
        }

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
