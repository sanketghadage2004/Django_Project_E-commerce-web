from venv import create
from django.shortcuts import redirect, render
from django.views import View
from product.models import ProductCategory
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as AuthLogin, logout as AuthLogout
from django.contrib.auth.models import User, auth
from frontend import urls


# Create your views here.
""" REGOSTER , LOGIN , LOGOUT  CLASSES"""

class Login(View):

    product_categories = ProductCategory.objects.filter(status=True)
    form_class = AuthenticationForm
    template_name = 'login.html'

    def get(self, request):
        form = self.form_class()

        context = {
        'product_categories':self.product_categories,
        'form':form,
        
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = self.form_class(data = request.POST)
        redirectURL = request.GET.get('next')
        if form.is_valid():
            AuthLogin(request, form.get_user())
            if redirectURL:
                return redirect(redirectURL)

            return redirect('home_page')
        context = {
            'product_categories':self.product_categories,
            'form':form
            }

        return render(request, self.template_name, context)
    

def logout(request):
    """  LOG OUT  """
    AuthLogout(request)
    return redirect('home_page')


def register(request):
    """ USER RREGISTRATION """
    product_categories = ProductCategory.objects.filter(status=True)
    if request.method =='POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']


        user = User.objects.create_user(first_name = first_name, last_name = last_name,  username = username, email = email, password = password1)
        user.save()
        
        return redirect('Login')
    else:
        return render(request, 'register.html',{'product_categories':product_categories})