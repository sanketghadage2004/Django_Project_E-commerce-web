from django.shortcuts import render
from .models import Post
# Create your views here.

def blog(request):
    posts = Post.objects.all()

    return render(request, 'blog.html', {'posts':posts})


def blogDetails(request):
    # posts = Post.objects.all()

    return render(request, 'blog_details.html')