import math

from django import template

register = template.Library()


@register.filter
def in_range(value, end_value=0):
    return range(math.ceil(value), int(end_value) + 1)


@register.filter
def get_rating_class(value, rating):
    """
    function that returns a class for a star object in rate.html
    :param value: star number 1-5
    :param rating: product rating, float, 1-5
    :return: class name "active" or "" or "semi-active"
    """
    if value <= math.floor(rating):
        return "active"
    elif abs(value - rating) < 1:
        return "semi-active"
    return ""
