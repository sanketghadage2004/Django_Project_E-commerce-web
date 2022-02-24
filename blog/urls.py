from django.urls import path
from blog import views


urlpatterns = [
    path('blog/', views.blog, name='blog'),
    path('blog-details', views.blogDetails, name='blog-details'),
    path('blog-details/<int:blog_id>', views.blogDetails, name='blog-details'),
]
