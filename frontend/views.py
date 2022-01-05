from django.shortcuts import render
from django.http import HttpResponse, request
from django.views import View
# Create your views here.

def home_page(request):
    return render(request, 'home.html')


class ProductListingView(View):

    def get(self, request):
        return render(request, 'product_listing.html') 