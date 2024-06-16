import jwt
from datetime import datetime

from django.db import models
from django.utils import timezone
from django.conf import settings

from client_portal.users import storage
from client_portal.users import constants


class UserPermission(models.Model):
    name = models.CharField(null=False, max_length=255, blank=False)
    enabled = models.BooleanField()


class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(null=False, max_length=255, blank=False)
    password = models.CharField(null=False, max_length=255, blank=False)
    name = models.CharField(null=False, max_length=511, blank=False)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)
    permissions = models.ManyToManyField(UserPermission)
    profile_picture = models.FileField(storage=storage.userStorage, upload_to=storage.UserStorageFolder, null=True, blank=True)
    deleted = models.DateTimeField(null=True)

    def delete(self, **kwargs):
        self.deleted = datetime.now()
        self.save()

    def is_admin(self):
        for permission in self.permissions.iterator():
            if permission.enabled and permission.name == constants.ADMIN:
                return True
        return False

    @staticmethod
    def decode_token(token):
        """Decode the access token from the Authorization header."""
        try:
            payload = jwt.decode(token, settings.get('SECRET'), algorithms='HS256')
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return "Expired token. Please log in to get a new token"
        except jwt.InvalidTokenError:
            return "Invalid token. Please register or login"
