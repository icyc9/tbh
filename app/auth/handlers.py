from http import HTTPStatus

from tornado.escape import json_decode

from app.base import BaseHandler
from app.exceptions import (AuthError, BadRequest)


class AuthHandler(BaseHandler):
    '''
    Base handler for the auth resource
    '''

    def initialize(self, auth_service, user_account_service, jwt_service):
        self.auth_service = auth_service
        self.user_service = user_account_service
        self.jwt_service = jwt_service

    def post(self):
        auth_header = self.request.headers.get('X-Verify-Credentials-Authorization')
        provider = self.request.headers.get('X-Auth-Service-Provider')

        if (not auth_header or not provider):
            raise BadRequest(reason='missing auth header and provider',
                             status_code=int(HTTPStatus.BAD_REQUEST))

        try:
            request_body = json_decode(self.request.body)
            gender = request_body['gender']
            push_id = request_body['push_id']
        except:
            raise BadRequest(reason='missing required fields', status_code=400)

        if gender not in (0, 1):
            raise BadRequest(reason='invalid gender provided', status_code=400)

        try:
            digits_user = self.auth_service.fetch_digits_provider(
                provider_url=provider, auth_header=auth_header)

            user_id = digits_user['id']
            phone_number = digits_user['phone_number']
        except AuthError:
            raise AuthError(reason='invalid user provided',
                            status_code=int(HTTPStatus.UNAUTHORIZED))


        self.user_service.verify_user_resource(
            user_id=user_id, phone_number=phone_number, gender=gender, push_id=push_id)

        jwt_token = self.jwt_service.sign_jwt_token({'id': user_id, 'push_id': push_id})

        response = {
            'token': jwt_token
        }

        self.write(response)
        self.set_status(int(HTTPStatus.CREATED))
        self.finish()