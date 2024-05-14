from django.core.validators import MinValueValidator
from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=50, blank=False, unique=True, verbose_name="Название категории")
    parent_category = models.ForeignKey('Category', null=True, blank=True,
                                        on_delete=models.SET_NULL, verbose_name="Родительская категория")


class Product(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False, verbose_name="Название")
    base_price = models.IntegerField(validators=[MinValueValidator(1)], null=False, blank=False,
                                     verbose_name="Основная цена")
    actual_price = models.IntegerField(validators=[MinValueValidator(1)], null=False, blank=False,
                                       verbose_name="Текущая цена с учётом возможных скидок")
    description = models.TextField(blank=False, null=False, verbose_name="Описание")
    category = models.ForeignKey('Category', null=True, on_delete=models.SET_NULL, blank=True,
                                 verbose_name="Категория")


def get_filename(instance, filename):
    extension = filename.split('.')[-1]
    if instance.pk:
        return 'products/{}.{}'.format(instance.pk, extension)
    else:
        return 'products/' + filename.encode("utf-8").decode()


class ProductImage(models.Model):
    product = models.ForeignKey('Product', null=False, on_delete=models.CASCADE, blank=False, verbose_name="Продукт")
    image = models.ImageField(verbose_name="Картинка", null=False, blank=False, upload_to=get_filename)
