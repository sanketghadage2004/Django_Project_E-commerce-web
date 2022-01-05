from django.urls import path
from frontend import views
urlpatterns = [
    path('',views.home_page, name='home_page'),
    path('product-listing-page/', views.ProductListingView.as_view(), name="ProductListingView")
]
