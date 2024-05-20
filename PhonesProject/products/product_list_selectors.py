from django.db.models import Avg, F
import random

from .models import Product


def get_discount_products():
    return Product.objects.annotate(price_difference=F('base_price') -
                                                     F('actual_price')).filter(price_difference__gt=0)\
               .order_by('-price_difference')[:4]


def get_rated_products():
    return Product.objects.all().annotate(rate=Avg('reviews__rate')).order_by('-rate')[:4]


def get_random_products():
    queryest = Product.objects.all()
    return random.sample(list(queryest), min(4, queryest.count()))


SIDE_LISTS = {  # показывать сбоку показывать на главной
    "Акция": (get_discount_products, True, False),
    'Продукты': (get_random_products, False, True),
    'Продукты с лучшей оценкой': (get_rated_products, True, True)}


def get_side_lists():
    return {i: (j[0](), j[1], j[2]) for i, j in SIDE_LISTS.items()}
