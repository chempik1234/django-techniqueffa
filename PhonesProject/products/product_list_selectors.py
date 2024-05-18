from django.db.models import Avg
import random

from .models import Product


def get_rated_products():
    return Product.objects.all().annotate(rate=Avg('reviews__rate')).order_by('-rate')[:4]


def get_random_products():
    queryest = Product.objects.all()
    return random.sample(list(queryest), min(4, queryest.count()))


SIDE_LISTS = {'Продукты': get_random_products,
              'Продукты с лучшей оценкой': get_rated_products}


def get_side_lists():
    return {i: j() for i, j in SIDE_LISTS.items()}
