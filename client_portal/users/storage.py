from uuid import uuid4

from django.utils.deconstruct import deconstructible

from client_portal.common import storage


@deconstructible
class UserStorageFolder(object):
    def __init__(self):
        pass

    def __call__(self, instance, name):
        return "users/{0}/{1}.{2}".format(
            instance.user_id,
            uuid4().hex,
            instance.ext
        )


class UserStorage(storage.BaseS3Storage):
    s3Key = storage.S3_KEY
    s3Secret = storage.S3_SECRET
    s3Bucket = storage.UPLOAD_BUCKET

    urlExpiration = 60 * 60 * 6  # 6 hours

    def friendlyUrl(self, name, fName, ext):
        return self._generateSignedUrl(Params={
            "Bucket": self.s3Bucket,
            "Key": name,
            'ResponseContentDisposition': 'attachment; filename=%s.%s' % (fName, ext)
            # Boto3 already escapes name
        },

            ExpiresIn=self.urlExpiration
        )


userStorage = UserStorage()