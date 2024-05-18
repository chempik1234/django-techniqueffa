from .models import Category
from .product_list_selectors import get_side_lists


def default_context(request):
    return {
        "side_lists": get_side_lists(),
        # 'categories': Category.objects.filter(parent_category=None)
    }
