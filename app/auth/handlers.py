from app.base import BaseHandler
from tornado.httpclient import AsyncHTTPClient, HTTPRequest


class AuthHandler(BaseHandler):
    '''
    Base handler for the auth resource
    '''

    def handle_auth_provider_response(self, response):
        print("\n")
        print(response.body)
        print("\n")

    '''Retrieve auth resource'''
    def post(self):
        auth_header = self.request.headers.get('X-Verify-Credentials-Authorization')
        provider = self.request.headers.get('X-Auth-Service-Provider')

        print(auth_header)
        print(provider)

        headers = {"Authorization": auth_header}

        http_client = AsyncHTTPClient()
        http_client.fetch(HTTPRequest(provider, headers=headers), self.handle_auth_provider_response)
