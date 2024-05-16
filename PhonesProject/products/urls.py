from django.urls import path, re_path
from .views import product_page, categories_view, subcategories_view, product_filter, \
                   post_review_view, delete_review_view, main_page

app_name = 'products'

urlpatterns = [
    path('', main_page, name="main_page"),
    re_path(r'product/(?P<product_id>\d+)/review/add/', post_review_view, name="add_review"),
    re_path(r'product/(?P<product_id>\d+)/review/delete/', delete_review_view, name="delete_review"),
    re_path(r'product/(?P<product_id>\d+)', product_page, name="product"),
    path('categories/<int:parent_category>/', subcategories_view, name='subcategories'),
    re_path(r'categories/', categories_view, name='category_submenu'),
    re_path(r'product/filter', product_filter, name="filter"),
]
