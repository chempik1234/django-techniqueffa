from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.html import format_html
from django.db.models import Avg

from rest_framework import serializers


class Category(models.Model):
    title = models.CharField(max_length=50, blank=False, unique=True, verbose_name="Название категории")
    parent_category = models.ForeignKey('Category', null=True, blank=True, related_name='children',
                                        on_delete=models.SET_NULL, verbose_name="Родительская категория")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        res = self.title
        if self.parent_category:
            res += " < " + self.parent_category.__str__()
        return res


class Product(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False, verbose_name="Название")
    base_price = models.FloatField(validators=[MinValueValidator(1)], null=False, blank=False,
                                   verbose_name="Основная цена")
    actual_price = models.FloatField(validators=[MinValueValidator(1)], null=False, blank=False,
                                     verbose_name="Текущая цена с учётом возможных скидок")
    description = models.TextField(blank=False, null=False, verbose_name="Описание")
    category = models.ForeignKey('Category', null=True, on_delete=models.SET_NULL, blank=True,
                                 verbose_name="Категория")

    def save_money(self):
        return self.base_price - self.actual_price

    def get_rate(self):
        average_rate = self.reviews.all().aggregate(avg_rate=Avg('rate'))['avg_rate']
        if average_rate is not None:
            return round(average_rate, 1)

    def get_reviews_amount(self):
        return self.reviews.all().count()

    def product_images(self):
        return ProductImageSerializer(self.images.all(), many=True).data

    def save_money_percent(self):
        return str(round((1 - self.actual_price / self.base_price) * 100, 1)) + " %"

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


def get_filename(instance, filename):
    extension = filename.split('.')[-1]
    if instance.pk:
        return 'products/{}.{}'.format(instance.pk, extension)
    else:
        return 'products/' + filename.encode("utf-8").decode()


class ProductImage(models.Model):
    product = models.ForeignKey('Product', null=False, on_delete=models.CASCADE, blank=False, verbose_name="Продукт",
                                related_name='images')
    image = models.ImageField(verbose_name="Картинка", null=False, blank=False, upload_to=get_filename)

    def __str__(self):
        title_html = '<p>{}</p>'
        image_html = '<img src="{}" style="max-width: 100px; max-height: 100px;" />'
        return format_html(title_html + image_html, self.product.title, self.image.url)

    class Meta:
        verbose_name = "Изображение продукта"
        verbose_name_plural = "Изображения продуктов"


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'actual_price', 'description', 'category']


class Review(models.Model):
    product = models.ForeignKey('Product', null=False, blank=False, on_delete=models.CASCADE, verbose_name="Продукт",
                                related_name="reviews")
    text = models.TextField(null=False, blank=True, verbose_name="Текст")
    rate = models.IntegerField(null=False, blank=False, validators=[MinValueValidator(1), MaxValueValidator(5)],
                               verbose_name="Оценка")
    author = models.ForeignKey('authentication.User', null=True, blank=False, on_delete=models.SET_NULL,
                               verbose_name="Автор")

    def __str__(self):
        return "Отзыв на " + self.product.title + "; оценка: " + str(self.rate)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        unique_together = ('author', 'product')
