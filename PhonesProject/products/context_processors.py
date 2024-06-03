from django.db.models import Q

from .models import Category
from .product_list_selectors import get_side_lists


def default_context(request):
    return {
        "side_lists": get_side_lists(),
        'footer_categories': Category.objects.filter(Q(children__isnull=True) |
                                                     Q(children__in=Category.objects.none())).distinct()
    }
