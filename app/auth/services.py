from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado import gen


class AuthService(object):

    '''
    Authentication service
    '''

    def __init__(self):
        self._http_client = AsyncHTTPClient()

    @gen.coroutine
    async def fetch_digits_provider(self, provider_url, headers):
        '''
        Fetch digits provider url and retrieve user account information.
        This method uses Tornado's underyling async http client to retrieve
        content asynchronously. Callback supplied will be called with data upon
        completion.
        '''

        response = await self._http_client.fetch(
            HTTPRequest(provider_url, headers=headers))

        return response.body