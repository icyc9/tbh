from http import HTTPStatus
from app.exceptions import JSONDecodeError

import tornado

from app.exceptions import ApiError


# Simple Tornado base handler with error handling
class BaseHandler(tornado.web.RequestHandler):
    '''
    Base handler class for all Request Handlers
    '''

    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)

    def write_error(self, status_code, **kwargs):

        error = kwargs['exc_info'][1]

        if status_code in [404]:
            self.write({'error': 'route not found'})
            self.finish()
        elif status_code == 405:
            self.write({'error': 'method not found'})
            self.finish()
        if isinstance(error, JSONDecodeError):
            # Error parsing json request body
            self.set_status(int(HTTPStatus.BAD_REQUEST))
            self.finish()
        elif isinstance(error, ApiError):
            # API Error
            self.write({'error': self._reason})
            self.set_status(status_code)
            self.finish()
        else:
            self.write({'error': 'an unknown error has occured'})
            self.finish()