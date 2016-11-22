from tornado.web import HTTPError
from json.decoder import JSONDecodeError


class AppError(Exception):
    '''Base class for all errors'''


class ApiError(AppError, HTTPError):
    '''Base class for all api errors'''

    def get_reason(self):
        return self._reason

    def get_status(self):
        return self.status_code


class ValidationError(ApiError):
    '''Validation error when input does not match json schema'''


class JSONDecodeError(ApiError):
    '''Error occurs when JSON is not able to be parsed'''


class ParseError(ApiError):
    '''Parse error'''


class ResourceError(ApiError):
    '''Error occurs when a resource does not exist'''


class AuthError(ApiError):
    '''Error occurs during authentication failure'''


class DuplicateMessage(ApiError):
    '''Error occurs when a duplicate tbh message is created'''


class PushNotifyError(ApiError):
    '''Error occurs when failed sending push notification'''


class PresetError(ApiError):
    '''Requested preset message does not exist'''


class BadRequest(ApiError):
    '''Occurs when an invalid request is received'''