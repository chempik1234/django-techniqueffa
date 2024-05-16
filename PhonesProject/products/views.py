from django.contrib.auth import login, logout
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from .forms import PriceForm, ReviewForm
from .models import Product, ProductImage, Category, Review
from .product_list_selectors import get_random_products, get_rated_products, get_side_lists


def main_page(request):
    data = settings.DEFAULT_CONTEXT.copy()
    data["title_header"] = None
    data["side_lists"] = get_side_lists()
    data['bg_color'] = 'light'
    return render(request, "products/main_page.html", context=data)


def product_page(request, product_id: int, form=None):
    data = settings.DEFAULT_CONTEXT.copy()
    product = get_object_or_404(Product, id=product_id)
    data["title_header"] = product.title
    data["product"] = product
    if form is None:
        form = ReviewForm()
    data['review_form'] = form
    data['your_review'] = Review.objects.filter(author=request.user, product__id=product_id).first()
    data["side_lists"] = get_side_lists()
    # data["product_images"] = ProductImageSerializer(product.images.all(), many=True).data
    return render(request, 'products/product.html', context=data)


def categories_view(request):
    return render(request, 'products/categories.html', context={'categories': Category.objects.filter(parent_category=None)})


def subcategories_view(request, parent_category):
    return render(request, 'products/categories.html',
                  context={'categories': Category.objects.filter(parent_category=parent_category)})


# def search_view(request):
#     query = request.GET
#     q = query.get('q')
#     return product_filter(request, q=q)


def try_get_int(var):
    if isinstance(var, str) and var.isdigit():
        return int(var)


def product_filter(request, q=None, order=None, price_min=None, price_max=None, category=None):
    query = request.GET

    if q is None:
        q = query.get('q')
    if category is None:
        category = try_get_int(query.get('category'))
    if order is None:
        order = try_get_int(query.get('order'))
    if price_min is None:
        price_min = try_get_int(query.get('price_min'))
    if price_max is None:
        price_max = try_get_int(query.get('price_max'))

    data = settings.DEFAULT_CONTEXT.copy()
    data["title_header"] = "Поиск"
    data["q"] = q
    data["category"] = category
    data["side_lists"] = get_side_lists()

    products = Product.objects.all()
    if category is not None:
        products = products.filter(category__pk=category)

    if q is not None:
        products = products.filter(title__icontains=q)

    if order == 0:
        products = products.order_by('actual_price')
        data["order"] = "Сначала дешёвые"
        data['order_num'] = order
    elif order == 1:
        products = products.order_by('-actual_price')
        data["order"] = "Сначала дорогие"
        data['order_num'] = order
    else:
        data["order"] = "Цена"

    if price_max is not None and price_min is not None:
        products = products.filter(actual_price__range=(price_min, price_max))
    elif price_min is not None:
        products = products.filter(actual_price__gte=price_min)
    elif price_max is not None:
        products = products.filter(actual_price__lte=price_max)

    data["products"] = products
    data["amount"] = products.count()
    data['price_form'] = PriceForm()
    return render(request, 'products/filter.html', context=data)


@require_POST
@login_required
def post_review_view(request, product_id):
    form = ReviewForm(request.POST)
    if form.is_valid():
        is_cool = form.save(request.user)
        if is_cool:
            messages.success(request, "Отзыв добавлен!")
        else:
            messages.error(request, "Отзыв не был добавлен!")
    else:
        return product_page(request, product_id, form)
    return HttpResponseRedirect('/product/' + str(product_id))


@require_POST
@login_required
def delete_review_view(request, product_id):
    review = Review.objects.filter(product__id=product_id, author=request.user)
    if review.exists():
        review.delete()
        messages.success(request, "Отзыв удалён!")
    else:
        messages.error(request, "Отзыв не был удалён!")
    return HttpResponseRedirect('/product/' + str(product_id))
    # return product_page(request, product_id)

