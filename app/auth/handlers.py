from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado import gen

from app.auth.services import AuthService
from app.base import BaseHandler


auth_service = AuthService()


class AuthHandler(BaseHandler):
    '''
    Base handler for the auth resource
    '''

    @gen.coroutine
    async def post(self):
        '''Create user resource'''

        auth_header = self.request.headers.get('X-Verify-Credentials-Authorization')
        provider = self.request.headers.get('X-Auth-Service-Provider')
        headers = {"Authorization": auth_header}

        response = await auth_service.fetch_digits_provider(
            provider_url=provider, headers=headers)

        self.write(response)
        self.set_status(201)
        self.finish()