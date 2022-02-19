from django.shortcuts import render
from .models import Post
from product.models import ProductCategory, Product

# Create your views here.

def blog(request):
    product_categories = ProductCategory.objects.filter(status=True)

    posts = Post.objects.all()

    return render(request, 'blog.html', {'posts':posts, 'product_categories':product_categories})


def blogDetails(request):
    product_categories = ProductCategory.objects.filter(status=True)

    # posts = Post.objects.all()

    return render(request, 'blog_details.html', {'product_categories':product_categories})