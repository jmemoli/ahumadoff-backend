from marshmallow import EXCLUDE
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.core import serializers

from middleware import authorizers
from middleware.exceptions import HttpError
from client_portal.users import services as user_services
from client_portal.users import schemas as user_schemas


class User(viewsets.ViewSet):
    @authorizers.authorized
    def get(self, request, **kwargs):
        try:
            user = kwargs['context']['user']
            if user.is_admin:
                users = user_services.retrieve_users()
                return Response(serializers.serialize('json', users), status=status.HTTP_200_OK)
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        except HttpError as e:
            return Response(status=e.status_code)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @authorizers.authorized
    def retrieve(self, request, pk, **kwargs):
        try:
            user = kwargs['context']['user']
            if user.id == pk:
                return Response(serializers.serialize('json', user), status=status.HTTP_200_OK)
            elif user.is_admin:
                user = user_services.retrieve_users(pk=pk)
                if user is None:
                    return Response(status=status.HTTP_404_NOT_FOUND)
                return Response(serializers.serialize('json', user), status=status.HTTP_200_OK)
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        except HttpError as e:
            return Response(status=e.status_code)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @authorizers.admin
    def create(self, request):
        try:
            data = user_schemas.CreateUserSchema().load(request.data, unknown=EXCLUDE)
            user = user_services.create_user(data)
            return Response(serializers.serialize('json', user), status=status.HTTP_200_OK)
        except HttpError as e:
            return Response(status=e.status_code)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @authorizers.authorized
    def destroy(self, request, pk, **kwargs):
        try:
            context = kwargs['context']
            user = context['user']
            if user.id != pk and not user.is_admin():
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            user_services.delete_user(pk)
            return Response(status=status.HTTP_200_OK)
        except HttpError as e:
            return Response(status=e.status_code)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @authorizers.authorized
    def update(self, request, pk, **kwargs):
        try:
            user = kwargs['context']['user']
            if user.id != pk:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            data = user_schemas.UpdateUserSchema().load(request.data, unknown=EXCLUDE)
            user = user_services.update_user(user, data)
            return Response(serializers.serialize('json', user), status=status.HTTP_200_OK)
        except HttpError as e:
            return Response(status=e.status_code)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)