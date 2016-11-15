from http import HTTPStatus

from tornado.escape import json_decode
from app.base import BaseHandler
from app.auth.jwt import jwt_required
from app.messages.schema import (PendingMessageSchema, MutualMessageSchema)
from app.presets.services import get_preset_by_code
from app.exceptions import DuplicateMessage


@jwt_required
class MessageHandler(BaseHandler):
    '''
    Base handler for the message resource
    '''

    def initialize(self, message_service):
        self.message_service = message_service

        self.FILTER_SERVICES = {
            'sent': self.message_service.get_sent_messages,
            'received': self.message_service.get_received_messages,
            'mutual': self.message_service.get_mutual_messages
        }

        self.FILTER_SERIALIZERS = {
            'sent': PendingMessageSchema,
            'received': PendingMessageSchema,
            'mutual': MutualMessageSchema
        }

    def get(self):
        '''Retrieve Message resource'''

        try:
            filter = self.get_argument("filter")
            filter_service = self.FILTER_SERVICES[filter]
        except:
            # Filter does not exist
            self.set_status(int(HTTPStatus.BAD_REQUEST))
            return self.finish()

        results = filter_service(self.tbh_user_id)
        # or to dump a list of objects
        message_schema = self.FILTER_SERIALIZERS[filter](many=True)
        results = {'messages': message_schema.dump(results).data }

        self.write(results)
        self.set_status(int(HTTPStatus.OK))
        self.finish()

    def post(self):
        '''Send message'''

        try:
            request_body = json_decode(self.request.body)
            receiver_phone_number = request_body['receiver_phone_number']
            message_text = get_preset_by_code(request_body['message_id'])
        except Exception as e:
            self.set_status(int(HTTPStatus.BAD_REQUEST))
            return self.finish()

        try:
            self.message_service.send_message(sender_id=self.tbh_user_id,
                receiver_phone_number=receiver_phone_number, text=message_text)
            
        except Exception:
            self.set_status(int(HTTPStatus.UNAUTHORIZED))
            return self.finish()
        except DuplicateMessage:
            self.set_status(int(HTTPStatus.CONFLICT))
            return self.finish()

        self.set_status(int(HTTPStatus.OK))
        self.finish()