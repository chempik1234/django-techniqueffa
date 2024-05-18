from django.urls import path, re_path
from .views import total_quantity, cart_add, cart_minimized, cart_clear, cart_remove, cart_details, OrderView, \
    result_view

app_name = 'cart'

urlpatterns = [
    path('total-quantity', total_quantity, name="total_quantity"),
    path('add', cart_add, name="add"),
    path('remove/<int:product_id>', cart_remove, name="remove"),
    path('clear', cart_clear, name="clear"),
    re_path('minimized', cart_minimized, name="minimized"),
    path('details', cart_details, name="details"),
    path('order', OrderView.as_view(), name="order_form"),
    path('result/<int:order_id>/<str:key>', result_view, name="result")
]
