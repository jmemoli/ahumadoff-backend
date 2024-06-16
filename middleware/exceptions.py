class HttpError(Exception):
    @property
    def status_code(self):
        """Defines the returned status_code"""
        raise NotImplementedError


class BadRequest(HttpError):
    status_code = 400


class Unauthorized(HttpError):
    status_code = 401


class Forbidden(HttpError):
    status_code = 403


class EntityNotFound(HttpError):
    status_code = 404


class Conflict(HttpError):
    status_code = 409


class InternalServerError(HttpError):
    status_code = 500
