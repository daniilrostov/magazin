from django.db import models

class ProductCategory(models.Model):
    name = models.CharField(max_length = 64, blank=True, null=True, default=None)
    is_active =  models.BooleanField(default=True)

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категория товаров'

class Product(models.Model):
    name = models.CharField(max_length = 64, blank=True, null=True, default=None)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    discount = models.IntegerField(default=0)
    category = models.ForeignKey(ProductCategory, blank=True, null=True, default=None)
    short_description = models.TextField(blank=True, null=True, default=None)
    description = models.TextField(blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)
    create = models.DateTimeField(auto_now_add=True, auto_now=False)
    update = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s, %s" % (self.name, self.price)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товар'

class ProductImage(models.Model):
    product = models.ForeignKey(Product, blank=True, null=True, default=None)
    image = models.ImageField(upload_to='img')
    is_main = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True, default=None)
    create = models.DateTimeField(auto_now_add=True, auto_now=False)
    update = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % (self.id)

    class Meta:
        verbose_name = 'Фотографии'
        verbose_name_plural = 'Фотографии'
