from client_portal.products.models import Product, ProductVariant
from middleware.exceptions import EntityNotFound, Conflict
from datetime import datetime
from django.db import IntegrityError


def retrieve_product(pk=None):
    products = Product.objects.filter(deleted__isnull=True)
    if pk is not None:
        products = products.filter(id=pk)
    if products.exists():
        for product in products:
            product.product_variants = product.product_variants.filter(deleted__isnull=True)
        if pk is not None:
            return products.first()
        return products
    raise EntityNotFound()


def update_product(pk, data):
    product = Product.objects.filter(pk=pk, deleted__isnull=True)
    if not product.exists():
        raise EntityNotFound()
    if data.name is not None:
        product.data = data.name
    if data.base_price is not None:
        product.base_price = data.base_price
    if data.description is not None:
        product.description = data.description
    try:
        product.save()
    except IntegrityError:
        raise Conflict()
    return product


def create_product(data):
    product = Product()
    product.name = data.name
    product.descrption = data.description
    product.base_price = data.base_price
    try:
        product.save()
    except IntegrityError:
        raise Conflict()
    return product


def delete_product(pk):
    product = Product.objects.filter(id=pk, deleted__isnull=True)
    product.deleted = datetime.now()
    product.save()


def retrieve_variant(pk=None):
    product_variant = ProductVariant.objects.filter(deleted__isnull=True)
    if pk is not None:
        product_variant = product_variant.filter(id=pk)
    if product_variant.exists():
        if pk is not None:
            return product_variant.first()
        return product_variant
    raise EntityNotFound()


def create_product_variant(pk, data):
    product_variant = ProductVariant()
    product_variant.product_id = pk
    product_variant.name = data.name
    product_variant.description = data.description
    product_variant.price = data.price
    try:
        product_variant.save()
    except IntegrityError:
        raise Conflict()
    return product_variant


def update_product_variant(pk, data):
    product_variant = ProductVariant.objects.filter(pk=pk, deleted__isnull=True)
    if not product_variant.exists():
        raise EntityNotFound()
    if data.name is not None:
        product_variant.data = data.name
    if data.price is not None:
        product_variant.price = data.price
    if data.description is not None:
        product_variant.description = data.description
    try:
        product_variant.save()
    except IntegrityError:
        raise Conflict()
    return product_variant


def delete_product_variant(pk):
    product_variant = ProductVariant.objects.filter(id=pk, deleted__isnull=True)
    product_variant.deleted = datetime.now()
    product_variant.save()
