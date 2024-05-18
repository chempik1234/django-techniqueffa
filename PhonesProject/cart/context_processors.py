from .cart import Cart


def default_context(request):
    return {'cart': Cart(request)}
