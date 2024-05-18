from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaulttags import url
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.decorators.http import require_POST
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .cart import Cart
from .forms import AddForm, AddressFormLite, OrderForm, PaymentForm, ShippingForm, EmailForm, BillingForm
from .models import Order, OrderToProduct


@login_required
def cart_minimized(request):
    return render(request, 'cart/minimized.html')


@login_required
def total_quantity(request):
    cart = Cart(request)
    return cart.__len__()


@login_required
@require_POST
def cart_add(request):
    form = AddForm(request.POST)
    if form.is_valid():
        amount = int(form.cleaned_data.get('amount'))
        key = int(form.cleaned_data.get('product_id'))
        cart = Cart(request)
        cart.add(key, amount)
        messages.success(request, f"Продукт добавлен в корзину x{amount} раз!")
    return redirect('cart:details')


@login_required
@require_POST
def cart_clear(request):
    cart = Cart(request)
    messages.success(request, f"Удалено x{cart.total_unique()}")
    cart.clear()
    return redirect('cart:details')


@login_required
@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    messages.success(request, f"Удалено x{cart.get_quantity_by_id(product_id)}")
    cart.remove(product_id)
    return redirect('cart:details')


@login_required
def cart_details(request):
    data = {"address_form_lite": AddressFormLite(),
            'title_header': 'Корзина'}
    return render(request, "cart/details.html", context=data)


@login_required
def result_view(request, order_id, key):
    # key = request.GET.get("key")
    order = products = None
    try:
        order = get_object_or_404(Order, pk=order_id, uuid=key)
        products = OrderToProduct.objects.filter(order=order)
    except ValidationError:
        pass
    data = {'order': order,
            'products': products,
            'title_header': "Оформление заказа"}
    # rendered_message = render_to_string('order_mail.html', {'order': order,
    #                                                         'products': products})

    # plain_message = strip_tags(rendered_message)
    # email_sent = send_mail(
    #     "Заказ",
    #     plain_message,
    #     settings.DEFAULT_FROM_EMAIL,
    #     [order.email],
    #     fail_silently=False,
    #     html_message=rendered_message
    # )
    # if email_sent == 1:
    #     messages.success(request, "Вам на почту " + order.email + " отправлено письмо!")
    # else:
    #     messages.error(request, "Вам на почту " + order.email + " должно было быть отправлено письмо, но "
    #                                                             "отправить не удалось!")
    return render(request, 'cart/result.html', context=data)


class OrderView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "cart/order_form.html"
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        query = request.GET
        # country = query.get('country')
        # city = query.get('city')
        # region = query.get('region')
        # post_index = query.get('post_index')

        # if country is None:
        #     country = ""
        # if city is None:
        #     city = ""
        # if region is None:
        #     region = ""
        # if post_index is None:
        #     post_index = ""
        return Response({'shipping_form': ShippingForm(),
                         'payment_form': PaymentForm(),
                         'billing_form': BillingForm(),
                         'email_form': EmailForm(),
                         'title_header': 'Оформление заказа'})

    def post(self, request):
        form = OrderForm(request.POST)
        if form.is_valid():
            cart = Cart(request)
            order = form.save(cart, request.user)
            if order:
                products = OrderToProduct.objects.filter(order=order)
                rendered_message = render_to_string('order_mail.html', {'order': order,
                                                                        'products': products})
                plain_message = strip_tags(rendered_message)
                email_sent = send_mail(
                    "Заказ",
                    plain_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [order.email],
                    fail_silently=False,
                    html_message=rendered_message
                )
                if email_sent == 1:
                    messages.success(request, "Вам на почту " + order.email + " отправлено письмо!")
                else:
                    messages.error(request, "Вам на почту " + order.email + " должно было быть отправлено письмо, но "
                                                                            "отправить не удалось!")
                cart.clear()
                return redirect('cart:result', order.pk, order.uuid)
            else:
                messages.error(request, "Неизвестная ошибка (не удалось сохранить заказ)")
            # for error in form.errors:
            #     messages.error(request, error)
        return Response({'shipping_form': ShippingForm(data=form.data),
                         'payment_form': PaymentForm(data=form.data),
                         'billing_form': BillingForm(data=form.data),
                         'email_form': EmailForm(data=form.data),
                         'title_header': 'Оформление заказа'})
