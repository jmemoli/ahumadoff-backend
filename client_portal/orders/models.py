from django.db import models
from client_portal.users.models import User
from client_portal.products.models import Product


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    price = models.DecimalField(blank=False, decimal_places=2, max_digits=10)
    currency = models.CharField(max_length=3, choices=[("UYU", "Pesos"), ("USD", "US Dollars")])
    address_street = models.CharField(max_length=127, null=False, blank=False)
    address_number = models.CharField(max_length=63, null=False, blank=False)
    address_extra = models.CharField(max_length=255, null=True)
    client_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    products = models.ManyToManyField(Product)
