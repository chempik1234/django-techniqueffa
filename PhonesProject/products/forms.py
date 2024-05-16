from django.contrib import admin
from django.forms import inlineformset_factory
from django import forms
from django.shortcuts import get_object_or_404
from django.utils.html import format_html

from .models import Product, ProductImage, Review


class ImagePreviewWidget(admin.widgets.AdminFileWidget):
    def render(self, name, value, attrs=None, renderer=None):
        output = []
        if value and getattr(value, "url", None):
            image_url = value.url
            output.append(format_html('<a href="{0}" target="_blank"><img src="{0}" style="max-width: 100px; max-height: 100px;" /></a>', image_url))
        output.append(super().render(name, value, attrs, renderer))
        return format_html(''.join(output))


ProductImageFormSet = inlineformset_factory(
    Product,
    ProductImage,
    fields=('image',),
    widgets={'image': ImagePreviewWidget},
    extra=1,
    can_delete=True,
)


class PriceForm(forms.Form):
    price_min = forms.FloatField(label="", min_value=0, max_value=999999, required=False,
                                 widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                 'placeholder': '≥ 0.00'}))
    price_max = forms.FloatField(label="", min_value=0, max_value=999999, required=False,
                                 widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                 'placeholder': '≤ 0.00'}))

    def clean_price_max(self):
        price_min = self.cleaned_data.get('price_min')
        if not price_min:
            raise forms.ValidationError("Минимальная цена некорректна!")
        price_max = self.cleaned_data['price_max']
        if price_max < price_min:
            raise forms.ValidationError('Максимальная цена меньше минимальной!')
        return price_max


class ReviewForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Всё отлично!'}),
                           required=True, label="Текст")
    rate = forms.IntegerField(required=True, min_value=1, max_value=5, widget=forms.HiddenInput(),
                              label="Оценка")
    product_id = forms.IntegerField(required=True, widget=forms.HiddenInput(), label="Продукт")

    def save(self, user):
        same_review = Review.objects.filter(product_id=self.cleaned_data['product_id'], author=user)
        if not same_review.exists():
            new_review = Review()
            new_review.author = user
            new_review.rate = self.cleaned_data['rate']
            new_review.text = self.cleaned_data['text']
            new_review.product = get_object_or_404(Product, id=self.cleaned_data['product_id'])
            new_review.save()
            return True

