from rest_framework.exceptions import APIException
from rest_framework import status
from django.utils.encoding import force_str


class ExceptionCodes:
    validationError = 'validationError'
    authenticationError = 'authenticationError'
    permissionError = 'permissionError'
    passwordChangeRequired = 'passwordChangeRequired'
    twoFARequired = 'twoFARequired'
    notFound = 'notFound'
    parseError = 'parseError'
    throttled = 'throttled'

    dbError = 'dbError'
    dataError = 'dataError'
    dataTooBig = 'dataTooBig'
    externalDbError = 'externalDbError'
    externalDataError = 'externalDataError'
    ssrsError = 'ssrsError'
    pdfError = 'pdfError'
    reloadError = 'reloadError'

    s3Error = 's3Error'
    emailSendingError = 'emailSendingError'

    unknownError = 'unknownError'
    operationError = 'operationError'


class OperationError(APIException):
    '''
        Custom exceptions that can not be served by regular API Exceptions.
        Exceptions will have:
           {
                detail: string, list or dictionary of strings ready.
                code: custom string code to identify the error when needed
                status_code: http status code to return, mostly used by web API, optional


           }
    '''
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Operation Error"
    code = ExceptionCodes.operationError

    def __init__(self, detail=None, code=None, statusCode=None):
        self.detail = _force_text_recursive(detail) if detail else None

        # Add message to base exception
        self.message = self.detail

        if statusCode:
            self.status_code = statusCode

        if code:
            self.code = code

    def __unicode__(self):
        return str(self.detail)


def _force_text_recursive(data):
    """
        Copied from library to also include tuples
    """
    if isinstance(data, (list,tuple)):
        return [
            _force_text_recursive(item) for item in data
        ]
    elif isinstance(data, dict):
        return dict([
            (key, _force_text_recursive(value))
            for key, value in data.items()
        ])
    return force_str(data, strings_only=False,errors='ignore')
