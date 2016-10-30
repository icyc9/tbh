from http import HTTPStatus

from tornado.escape import json_decode

from app.base import BaseHandler
from app.exceptions import AuthError


class AuthHandler(BaseHandler):
    '''
    Base handler for the auth resource
    '''

    def initialize(self, auth_service, user_account_service, jwt_service):
        self.auth_service = auth_service
        self.user_service = user_account_service
        self.jwt_service = jwt_service

    async def post(self):
        auth_header = self.request.headers.get('X-Verify-Credentials-Authorization')
        provider = self.request.headers.get('X-Auth-Service-Provider')
        print(self.request.headers.get('Content-Type'))
        if (not auth_header or not provider):
            self.set_status(HTTPStatus.BAD_REQUEST)
            return self.finish()

        try:
            request_body = json_decode(self.request.body)
            gender = request_body['gender']

            if gender not in (0, 1):
                raise Exception('Invalid gender')
        except Exception as e:
            self.set_status(HTTPStatus.BAD_REQUEST)
            return self.finish()


        try:
            digits_user = await self.auth_service.fetch_digits_provider(
                provider_url=provider, auth_header=auth_header)

            user_id = digits_user['id']
            phone_number = digits_user['phone_number']

        except AuthError:
            self.set_status(HTTPStatus.UNAUTHORIZED)
            return self.finish()

        self.user_service.verify_user_resource(
            user_id=user_id, phone_number=phone_number, gender=gender)

        jwt_token = self.jwt_service.sign_jwt_token({'id': user_id})

        response = {
            'token': jwt_token
        }

        self.write(response)
        self.set_status(HTTPStatus.CREATED)
        self.finish()