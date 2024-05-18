import re
from django import forms
from .models import Order, OrderToProduct


class AddForm(forms.Form):
    product_id = forms.IntegerField(required=True, widget=forms.HiddenInput())
    amount = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={"class": "form-control",
                                                                               "placeholder": "",
                                                                               "value": "1"}),
                                min_value=1)


class AddressFormLite(forms.Form):
    country = forms.CharField(label="", required=True, widget=forms.TextInput(attrs={'class': 'form-control mt-1',
                                                                                     'placeholder': 'Страна'}),
                              max_length=100)
    city = forms.CharField(label="", required=True, widget=forms.TextInput(attrs={'class': 'form-control mt-1',
                                                                                  'placeholder': 'Город'}),
                           max_length=100)
    region = forms.CharField(label="", required=True, widget=forms.TextInput(attrs={'class': 'form-control mt-1',
                                                                                    'placeholder': 'Область/регион'}),
                             max_length=100)
    post_index = forms.CharField(label="",
                                 required=True,
                                 widget=forms.TextInput(attrs={'class': 'form-control mt-1 text-uppercase',
                                                               'placeholder': 'Почтовый индекс'}), min_length=6,
                                 max_length=6)

    def clean_post_index(self):
        post_index = self.cleaned_data['post_index'].upper()
        if len(post_index) != 6:
            raise forms.ValidationError("Длина почтового индекса должна быть равна 6!")
        pattern = "^[А-Я0-9]+$"
        if not bool(re.match(pattern, post_index)):
            raise forms.ValidationError("Пользователя с такой почтой нет!")
        return post_index


class ShippingForm(AddressFormLite):
    name = forms.CharField(label="", required=True, widget=forms.TextInput(attrs={'class': 'form-control mt-1',
                                                                                  'placeholder': 'Имя'}),
                           max_length=50)
    surname = forms.CharField(label="", required=True, widget=forms.TextInput(attrs={'class': 'form-control mt-1',
                                                                                     'placeholder': 'Фамилия'}),
                              max_length=50)
    address = forms.CharField(label="", required=True, widget=forms.TextInput(attrs={'class': 'form-control mt-1',
                                                                                     'placeholder': 'Адрес'}),
                              max_length=255)
    additional_to_house = forms.CharField(label="", required=False,
                                          widget=forms.TextInput(attrs={'class': 'form-control mt-1',
                                                                        'placeholder': 'Крыло/подъезд/этаж/квартира'
                                                                                       ' (необязательно)'}),
                                          max_length=100)
    phone = forms.CharField(label="", required=False,
                            widget=forms.TextInput(attrs={'class': 'form-control mt-1',
                                                          'placeholder': 'Телефон'
                                                                         ' (необязательно)'}),
                            max_length=20)


class BillingForm(forms.Form):
    billing_country = forms.CharField(label="", required=True,
                                      widget=forms.TextInput(attrs={'class': 'form-control mt-1',
                                                                    'placeholder': 'Страна'}),
                                      max_length=100)
    billing_city = forms.CharField(label="", required=True,
                                   widget=forms.TextInput(attrs={'class': 'form-control mt-1',
                                                                 'placeholder': 'Город'}),
                                   max_length=100)
    billing_region = forms.CharField(label="", required=True,
                                     widget=forms.TextInput(attrs={'class': 'form-control mt-1',
                                                                   'placeholder': 'Область/регион'}),
                                     max_length=100)
    billing_post_index = forms.CharField(label="",
                                         required=True,
                                         widget=forms.TextInput(attrs={'class': 'form-control mt-1 text-uppercase',
                                                                       'placeholder': 'Почтовый индекс'}), min_length=6,
                                         max_length=6)
    billing_name = forms.CharField(label="", required=True, widget=forms.TextInput(attrs={'class': 'form-control mt-1',
                                                                                          'placeholder': 'Имя'}),
                                   max_length=50)
    billing_surname = forms.CharField(label="", required=True,
                                      widget=forms.TextInput(attrs={'class': 'form-control mt-1',
                                                                    'placeholder': 'Фамилия'}),
                                      max_length=50)
    billing_address = forms.CharField(label="", required=True,
                                      widget=forms.TextInput(attrs={'class': 'form-control mt-1',
                                                                    'placeholder': 'Адрес'}),
                                      max_length=255)
    billing_additional_to_house = forms.CharField(label="", required=False,
                                                  widget=forms.TextInput(attrs={'class': 'form-control mt-1',
                                                                                'placeholder': 'Крыло/подъезд/этаж/ква'
                                                                                               'ртира (необязатель'
                                                                                               'но)'}),
                                                  max_length=100)
    billing_phone = forms.CharField(label="", required=False,
                                    widget=forms.TextInput(attrs={'class': 'form-control mt-1',
                                                                  'placeholder': 'Телефон'
                                                                                 ' (необязательно)'}),
                                    max_length=20)
    billing_use_billing = forms.BooleanField(label="Использовать этот же адрес для выставления счетов",
                                             widget=forms.CheckboxInput(attrs={'class': 'custom-control-input',
                                                                               'checked': ''}),
                                             required=False)

    def clean_post_index(self):
        post_index = self.cleaned_data['post_index'].upper()
        if len(post_index) != 6:
            raise forms.ValidationError("Длина почтового индекса должна быть равна 6!")
        pattern = "^[А-Я0-9]+$"
        if not bool(re.match(pattern, post_index)):
            raise forms.ValidationError("Пользователя с такой почтой нет!")
        return post_index


class EmailForm(forms.Form):
    email = forms.EmailField(label="", required=False, widget=forms.EmailInput(attrs={'class': 'form-control mt-1',
                                                                                      'placeholder': 'Email'}))


class PaymentForm(forms.Form):
    payment_type = forms.ChoiceField(label="", required=False, choices=((False, "Оплатить сейчас банковским переводом"),
                                                                        (True, "Оплатить при получении")),
                                     widget=forms.RadioSelect())


class NoteForm(forms.Form):
    note = forms.CharField(label="", required=False, widget=forms.TextInput(attrs={'class': 'form-control m-2',
                                                                                   'placeholder': "Примечания к заказу,"
                                                                                                  "например, особые пож"
                                                                                                  "елания отделу достав"
                                                                                                  "ки"}),
                           max_length=100)
    add_note = forms.BooleanField(required=False, label="Добавить примечание к заказу",
                                  widget=forms.CheckboxInput(attrs={'class': 'custom-control-input'}))


class OrderForm(ShippingForm, EmailForm, PaymentForm, NoteForm, BillingForm):
    def save(self, cart, user):
        order_data = {
            'billing_country': self.cleaned_data['billing_country'],
            'billing_city': self.cleaned_data['billing_city'],
            'billing_region': self.cleaned_data['billing_region'],
            'billing_post_index': self.cleaned_data['billing_post_index'],
            'billing_name': self.cleaned_data['billing_name'],
            'billing_surname': self.cleaned_data['billing_surname'],
            'billing_address': self.cleaned_data['billing_address'],
            'billing_additional_to_house': self.cleaned_data['billing_additional_to_house'],
            'billing_phone': self.cleaned_data['billing_phone'],
            'payment_type': self.cleaned_data['payment_type'],
            'email': self.cleaned_data['email'],
            'country': self.cleaned_data['country'],
            'city': self.cleaned_data['city'],
            'region': self.cleaned_data['region'],
            'post_index': self.cleaned_data['post_index'],
            'name': self.cleaned_data['name'],
            'surname': self.cleaned_data['surname'],
            'address': self.cleaned_data['address'],
            'additional_to_house': self.cleaned_data['additional_to_house'],
            'phone': self.cleaned_data['phone'],
            'note': self.cleaned_data.get('note', None),
        }
        if not order_data.get('email'):
            order_data['email'] = user.email
        order_instance = Order(**order_data)
        order_instance.save()
        for i in cart:
            otp = OrderToProduct()
            otp.order = order_instance
            otp.product = i[1][0]
            otp.quantity = i[1][1]
            otp.save()
        return order_instance
