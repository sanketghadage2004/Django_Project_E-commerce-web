from django.urls import path
from django.views.generic.base import View
from frontend import views
urlpatterns = [
    path('',views.home_page, name='home_page'),

    path('product-listing-page/', views.ProductListingView.as_view(), name="ProductListingView"),

    path('product-listing-page/<int:product_category_id>', views.ProductListingView.as_view(), name="ProductListingView"),
    
    path('product-details/<int:product_id>', views.ProductDetailsView.as_view(), name="ProductDetailsView"),
    path('contact/',views.contact, name= 'contact'),
    # path('login', views.test_login)
]
