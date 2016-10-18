from json.decoder import JSONDecodeError


class AppError(Exception):
    '''Base class for all errors'''


class ValidationError(AppError):
    '''Validation error when input does not match json schema'''


class JSONDecodeError(AppError):
    '''Error occurs when JSON is not able to be parsed'''


class ParseError(AppError):
    '''Parse error'''