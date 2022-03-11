
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frontend.urls')),
    path('cart/', include('cart.urls')),
    path('auth/', include('authentication.urls')),
    path('accounts/', include('authentication.urls')),
    path('blog/',include('blog.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
