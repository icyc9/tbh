def format_repr(obj, attributes) -> str:
    """Format an object's repr method with specific attributes."""

    attribute_repr = ', '.join(('{}={}'.format(attr, repr(getattr(obj, attr)))
                                for attr in attributes))
    return "{0}({1})".format(obj.__class__.__qualname__, attribute_repr)


def format_api_error_message(message, **kwargs):
    '''Format for API error messages'''

    return {'error': message, **kwargs}