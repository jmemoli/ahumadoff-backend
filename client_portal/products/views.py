from marshmallow import EXCLUDE
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.core import serializers

from middleware import authorizers
from middleware.exceptions import HttpError
from client_portal.products import services as product_services
from client_portal.products.schemas import (
    UpdateProductSchema,
    CreateProductSchema,
    CreateProductVariantSchema,
    UpdateProductVariantSchema
)


class Product(viewsets.ViewSet):
    def retrieve(self, request, pk, **kwargs):
        try:
            product = product_services.retrieve_product(pk)
            return Response(serializers.serialize('json', product), status=status.HTTP_200_OK)
        except HttpError as e:
            return Response(status=e.status_code)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, **kwargs):
        try:
            product = product_services.retrieve_product()
            if product is None:
                return Response(status=status.HTTP_404_NOT_FOUND)
            return Response(serializers.serialize('json', product), status=status.HTTP_200_OK)
        except HttpError as e:
            return Response(status=e.status_code)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @authorizers.authorized
    def update(self, request, pk, **kwargs):
        try:
            data = UpdateProductSchema().load(request.data, unknown=EXCLUDE)
            product = product_services.update_product(pk, data)
            return Response(serializers.serialize('json', product), status=status.HTTP_200_OK)
        except HttpError as e:
            return Response(status=e.status_code)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @authorizers.authorized
    def create(self, request, **kwargs):
        try:
            data = CreateProductSchema().load(request.data, unknown=EXCLUDE)
            product = product_services.create_product(data)
            return Response(serializers.serialize('json', product), status=status.HTTP_201_CREATED)
        except HttpError as e:
            return Response(status=e.status_code)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @authorizers.authorized
    def delete(self, request, pk, **kwargs):
        try:
            product_services.delete_product(pk)
            return Response(status=status.HTTP_200_OK)
        except HttpError as e:
            return Response(status=e.status_code)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve_variant(self, request, pk, **kwargs):
        try:
            product_variant = product_services.retrieve_variant(pk)
            return Response(serializers.serialize('json', product_variant), status=status.HTTP_200_OK)
        except HttpError as e:
            return Response(status=e.status_code)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_variant(self, request, **kwargs):
        try:
            product_variants = product_services.retrieve_variant()
            return Response(serializers.serialize('json', product_variants), status=status.HTTP_200_OK)
        except HttpError as e:
            return Response(status=e.status_code)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @authorizers.authorized
    def create_variant(self, request, pk, **kwargs):
        try:
            data = CreateProductVariantSchema().load(request.data, unknown=EXCLUDE)
            product_variant = product_services.create_product_variant(pk, data)
            return Response(serializers.serialize('json', product_variant), status=status.HTTP_200_OK)
        except HttpError as e:
            return Response(status=e.status_code)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @authorizers.authorized
    def update_variant(self, request, pk, **kwargs):
        try:
            data = UpdateProductVariantSchema().load(request.data, unknown=EXCLUDE)
            product_variant = product_services.update_product_variant(pk, data)
            return Response(serializers.serialize('json', product_variant), status=status.HTTP_200_OK)
        except HttpError as e:
            return Response(status=e.status_code)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @authorizers.authorized
    def delete_variant(self, request, pk, **kwargs):
        try:
            product_services.delete_product_variant(pk)
            return Response(status=status.HTTP_200_OK)
        except HttpError as e:
            return Response(status=e.status_code)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
