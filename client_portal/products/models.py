from django.db import models


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(null=False, max_length=255, blank=False, unique=True)
    base_price = models.DecimalField(blank=False, decimal_places=2, max_digits=10)
    description = models.CharField(null=False, max_length=4095, blank=False)
    deleted = models.DateTimeField(null=True)


class ProductVariant(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    name = models.CharField(null=False, max_length=255, blank=False)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    description = models.CharField(max_length=4095)
    deleted = models.DateTimeField(null=True)

    class Meta:
        unique_together = ('product_id', 'name')
