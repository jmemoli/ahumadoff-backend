from django.conf import settings
from django.contrib.auth.hashers import make_password

from client_portal.users.models import User
from middleware.exceptions import EntityNotFound


def create_user(data):
    user = User()
    user.username = data.username
    user.password = make_password(data.password, hasher=settings.SECRET)
    user.name = data.name
    user.save()
    return user


def retrieve_users(pk=None):
    if pk is not None:
        user = User.objects.get(id=pk)
        return user
    users = User.objects.filter(deleted__isnull=True)
    return users


def update_user(user, data):
    if data.username is not None:
        user.username = data.username
    if data.password is not None:
        user.password = make_password(data.password, hasher=settings.SECRET)
    if data.name is not None:
        user.name = data.name
    user.save()
    return user


def delete_user(pk):
    user = User.objects.get(id=pk)
    if user is None:
        raise EntityNotFound()
    user.delete()
