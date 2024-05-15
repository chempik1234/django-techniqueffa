from django.contrib.auth import login, logout
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from .forms import PriceForm
from .models import Product, ProductImage, Category
from .serializers import ProductImageSerializer


def product_page(request, product_id: int):
    data = settings.DEFAULT_CONTEXT.copy()
    product = get_object_or_404(Product, id=product_id)
    data["title_header"] = product.title
    data["product"] = product
    data["product_images"] = ProductImageSerializer(product.images.all(), many=True).data
    return render(request, 'products/product.html', context=data)


def categories_view(request):
    return render(request, 'products/categories.html', context={'categories': Category.objects.all()})


def subcategories_view(request, parent_category):
    return render(request, 'products/categories.html',
                  context={'categories': Category.objects.filter(parent_category=parent_category)})


def search_view(request):
    query = request.GET
    q = query.get('q')
    return product_filter(request, q=q)


def product_filter(request, q=None, category=None, order=None):
    query = request.GET
    if q is None:
        q = query.get('q')
    if category is None:
        category = query.get('category')
        if isinstance(category, str) and category.isdigit():
            category = int(category)
        else:
            category = None
    if order is None:
        order = query.get('order')
        if isinstance(order, str) and order.isdigit():
            order = int(order)
        else:
            order = None

    data = settings.DEFAULT_CONTEXT.copy()
    data["title_header"] = "Поиск"
    data["q"] = q
    data["category"] = category

    products = Product.objects.all()
    if category is not None:
        products = products.filter(category__pk=category)
    if q is not None:
        products = products.filter(title__icontains=q)
    if order == 0:
        products = products.order_by('actual_price')
        data["order"] = "Сначала дешёвые"
    elif order == 1:
        products = products.order_by('-actual_price')
        data["order"] = "Сначала дорогие"
    else:
        data["order"] = "Цена"
    data["products"] = products
    data["amount"] = len(products)
    data['price_form'] = PriceForm()
    return render(request, 'products/filter.html', context=data)
