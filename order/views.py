from multiprocessing import context
from re import template
from django.shortcuts import render
from django.views import View

# Create your views here.

class MyOrder(View):
    """display all order of logged in user"""
    # use decorator in this ""logged in required""
    template_name=" "
    def get(self,request):


        context={


        }
        return render(request,self.template_name, context)


class OrderDetails(View):
    """display  order detail of of selected_id"""
    template_name=" "
    def get(self,request):


        context={


        }
        return render(request,self.template_name, context)