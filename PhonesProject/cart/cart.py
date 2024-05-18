from django.conf import settings
from products.models import Product  # , ProductSerializer


def cart_item_convert(key, quantity):
    product = Product.objects.get(id=key)
    return [product, quantity]


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}  # { product_id: quantity, ... }
        self.cart = cart

    # def delete_wrong_items(self, func):
    #     for key, item in self.cart.items():
    #         if not isinstance(key, int) or not isinstance(item, tuple):
    #             self.cart.pop(key)
    #         elif

    def __iter__(self):
        for product_id, quantity in self.cart.items():
            yield product_id, cart_item_convert(product_id, quantity)

    # @delete_wrong_items
    def __len__(self):
        """
        Sum up the quantity
        """
        return sum(i for i in self.cart.values())

    def total_quantity(self):
        return self.__len__()

    def total_unique(self):
        return len([i for i in self.cart.keys() if isinstance(self.cart[i], int)])

    def get_quantity_by_id(self, key):
        obj = self.cart.get(key)
        if not obj:
            obj = self.cart.get(str(key))
        if obj:
            return obj

    def display_amount(self):
        return f"{self.total_unique()} ({self.total_quantity()})"

    def add(self, product_id, quantity=1):
        """
        Add item to cart and update the quantity
        """
        product = Product.objects.filter(id=product_id)
        if product.exists():
            # product = product.first()
            key = str(product_id)
            if not self.cart.get(key):
                self.cart[key] = 0
            self.cart[key] += quantity
            self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product_id):
        if self.cart.get(str(product_id)):
            del self.cart[str(product_id)]
            self.save()

    def get_total_price(self):
        return sum(cart_item_convert(key, quantity)[0].actual_price * quantity for key, quantity in self.cart.items()
                   if isinstance(quantity, int))

    def clear(self):
        self.cart = {}
        self.save()
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def is_empty(self):
        if not self.cart:
            return True
        else:
            return False

    def get_obj_by_int_key(self, key):
        obj = self.cart.get(key)
        if not obj:
            key = str(key)
            obj = self.cart.get(key)
        if obj:
            return obj
