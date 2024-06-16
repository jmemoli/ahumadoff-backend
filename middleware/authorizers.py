import functools
from rest_framework import status
from rest_framework.response import Response
from client_portal.users.models import User
from client_portal.users import constants


def authorized(func):
    @functools.wraps(func)
    def wrapper_authorized(*args, **kwargs):
        token = get_token_from_raw_authorization(args[0].headers.get('Authorization', None))
        if not token:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        user_id = User.decode_token(token)
        if not isinstance(user_id, int):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=user_id)
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if kwargs.get("context") is not None:
            kwargs["context"]["user"] = user
        else:
            kwargs["context"] = {"user": user}

        return func(*args, **kwargs)
    return wrapper_authorized


def admin(func):
    @functools.wraps(func)
    def wrapper_authorized(*args, **kwargs):
        token = get_token_from_raw_authorization(args[0].headers.get('Authorization', None))
        if not token:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        user_id = User.decode_token(token)
        if not isinstance(user_id, int):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=user_id)
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND)

        permissions = User.permissions
        for permission in permissions.iterator():
            if permission.enabled and permission.name == constants.ADMIN:
                if kwargs.get("context") is not None:
                    kwargs["context"]["user"] = user
                else:
                    kwargs["context"] = {"user": user}
                return func(*args, **kwargs)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    return wrapper_authorized


def get_token_from_raw_authorization(raw_token):
    if raw_token is None or raw_token == "":
        return None
    raw_token_sections = raw_token.split(' ')
    if len(raw_token_sections) < 2:
        return None
    return raw_token_sections[1]
