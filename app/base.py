import tornado


# Simple Tornado base handler with error handling
class BaseHandler(tornado.web.RequestHandler):
    '''
    Base handler class for all Request Handlers
    '''

    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)

    def write_error(self, status_code, **kwargs):
        self.set_status(status_code)

        if status_code in [404]:
            self.write({'error': 'route not found'})
        elif status_code == 405:
            self.write({'error': 'method not found'})
        else:
            self.write({'error': 'an unknown error has occured'})