from app.exceptions import ParseError


def parse_tornado_url_arguments(get_argument_fn, expected_params):
    '''
    Retrieve all expected parameters using Tornado get_argument
    method
    '''

    parsed_args = {}

    for param in expected_params:
        arg = get_argument_fn(param, expected_params[param], True)

        if not arg:
            raise ParseError('Invalid arguments')

        parsed_args[param] = arg

    return parsed_args