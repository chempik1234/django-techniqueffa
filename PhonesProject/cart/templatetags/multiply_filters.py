from django import template

register = template.Library()


@register.filter
def multiply(value, multiplier):
    return value * multiplier
