from django.core.validators import MinValueValidator
from django.db import models
import uuid

from django.db.models import Sum, F


class Order(models.Model):
    billing_country = models.CharField(max_length=100)
    billing_city = models.CharField(max_length=100)
    billing_region = models.CharField(max_length=100)
    billing_post_index = models.CharField(max_length=6)
    billing_name = models.CharField(max_length=50)
    billing_surname = models.CharField(max_length=50)
    billing_address = models.CharField(max_length=255)
    billing_additional_to_house = models.CharField(max_length=100, blank=True, null=True)
    billing_phone = models.CharField(max_length=20, blank=True, null=True)
    payment_type = models.BooleanField()
    email = models.EmailField()
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    post_index = models.CharField(max_length=6)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    additional_to_house = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    note = models.CharField(max_length=100, blank=True, null=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    date = models.DateField(auto_now=True)

    def address_segments(self):
        return [self.country, self.region, self.city, self.address, self.post_index, self.additional_to_house,
                self.email, self.name, self.surname, self.phone]

    def billing_segments(self):
        return [self.billing_country, self.billing_region, self.billing_city, self.billing_address, self.billing_post_index, self.billing_additional_to_house,
                self.billing_name, self.billing_surname, self.billing_phone]

    def payment_type_str(self):
        if self.payment_type:
            return "Оплата при доставке"
        else:
            return "Оплата банковским переводом"

    def get_total_price(self):
        return self.products.all().aggregate(sum=Sum(F("product__actual_price") * F("quantity"))).get('sum', 0)


class OrderToProduct(models.Model):
    order = models.ForeignKey('Order', related_name="products", null=False, on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', null=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False, validators=[MinValueValidator(1)])

    def get_price(self):
        return self.product.actual_price * self.quantity
