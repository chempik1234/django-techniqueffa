from django.contrib import admin

from .forms import ProductImageFormSet
from .models import ProductImage, Product, Category
from .forms import ProductImageFormSet


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    formset = ProductImageFormSet
    extra = 1
    can_delete = True


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category_title')
    inlines = [ProductImageInline]
    model = Product

    def category_title(self, obj):
        return obj.category.title


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent_category_if_so')
    model = Category

    def parent_category_if_so(self, obj):
        if obj.parent_category:
            return obj.parent_category.title
        else:
            return "-"


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductImage)
