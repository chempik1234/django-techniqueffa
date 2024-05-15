from django.urls import path, re_path
from .views import product_page, categories_view, subcategories_view, search_view, product_filter

app_name = 'products'

urlpatterns = [
    re_path(r'product/(?P<product_id>\d+)', product_page),
    path('categories/<int:parent_category>/', subcategories_view, name='subcategories'),
    re_path(r'categories/', categories_view, name='category_submenu'),
    path('product/search', search_view, name="search"),
    path('product/filter', product_filter, name="filter")
]
