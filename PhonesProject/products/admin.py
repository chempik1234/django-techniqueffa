from django.contrib import admin

from .models import ProductImage, Product, Category

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(ProductImage)
