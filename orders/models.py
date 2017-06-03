from django.db import models
from products.models import Product
from django.db.models.signals import post_save

class Status(models.Model):
    name = models.CharField(max_length=28, blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)
    create = models.DateTimeField(auto_now_add=True, auto_now=False)
    update = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "Статус %s" % (self.name)

    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статус заказа'

class Order(models.Model):
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    custumer_name = models.CharField(max_length = 128)
    custumer_email = models.EmailField(blank=True, null=True, default=None)
    custumer_phone = models.CharField(max_length = 48, blank=True, null=True, default=None)
    comments = models.TextField(blank=True, null=True, default=None)
    status = models.ForeignKey(Status)
    create = models.DateTimeField(auto_now_add=True, auto_now=False)
    update = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s, %s" % (self.id, self.status.name)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказ'


class ProductInOrder(models.Model):
    order = models.ForeignKey(Order, blank=True, null=True, default=None)
    product = models.ForeignKey(Product, blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)
    nmb = models.IntegerField(default=1)
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    create = models.DateTimeField(auto_now_add=True, auto_now=False)
    update = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % (self.product.name)

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товар в заказе'

    def save(self, *args, **kwargs):
        price_per_item = self.product.price
        self.price_per_item = price_per_item
        self.total_price = self.nmb * self.price_per_item

        super(ProductInOrder, self).save(*args, **kwargs)

def product_in_order_post_save(sender, instance, created, **kwargs):
    order = instance.order
    all_products_in_order = ProductInOrder.objects.filter(order=order, is_active=True)

    order_total_price = 0
    for item in all_products_in_order:
        order_total_price += item.total_price

    instance.order_total_price = order_total_price
    instance.order.save(force_update=True)
post_save.connect(product_in_order_post_save, sender=ProductInOrder)
