from django.contrib import admin
from django.forms import inlineformset_factory
from django import forms
from django.utils.html import format_html

from .models import Product, ProductImage


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
    price_min = forms.FloatField(label="", min_value=0, max_value=999999,
                                 widget=forms.NumberInput(attrs={'class': 'form-control mr-1',
                                                                 'placeholder': '≥ 0.00'}))
    price_max = forms.FloatField(label="", min_value=0, max_value=999999,
                                 widget=forms.NumberInput(attrs={'class': 'form-control mr-1',
                                                                 'placeholder': '≤ 0.00'}))

    def clean_price_max(self):
        price_min = self.cleaned_data.get('price_min')
        if not price_min:
            raise forms.ValidationError("Минимальная цена некорректна!")
        price_max = self.cleaned_data['price_max']
        if price_max < price_min:
            raise forms.ValidationError('Максимальная цена меньше минимальной!')
        return price_max
