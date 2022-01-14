from django.shortcuts import redirect, render
from django.views import View
from product.models import ProductCategory
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as AuthLogin, logout as AuthLogout
# Create your views here.
class Login(View):

    product_categories = ProductCategory.objects.filter(status=True)
    form_class = AuthenticationForm
    template_name = 'login.html'

    def get(self, request):
        form = self.form_class()

        context = {
        'product_categories':self.product_categories,
        'form':form
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = self.form_class(data = request.POST)
        if form.is_valid():
            AuthLogin(request, form.get_user())
            return redirect('home_page')
        context = {
            'product_categories':self.product_categories,
            'form':form
            }

        return render(request, self.template_name, context)
    

def logout(request):
    AuthLogout(request)
    return redirect('Login')