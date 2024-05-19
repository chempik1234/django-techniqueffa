"""
URL configuration for PhonesProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.template.defaulttags import url
from django.urls import path, re_path, include
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authentication.urls', namespace='authentication')),
    path('', include('products.urls', namespace='products')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('', include('static_pages.urls', namespace='static_pages')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

# urlpatterns += [
#     re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
#     # re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT})
# ]

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

print('Urls.py MEDIA_ROOT: %s' % settings.MEDIA_ROOT)
print('Urls.py STATIC_ROOT: %s' % settings.STATIC_ROOT)
