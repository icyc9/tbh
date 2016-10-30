from http import HTTPStatus

from tornado.escape import json_decode
from app.base import BaseHandler
from app.auth.jwt import jwt_required
from app.messages.schema import MessageSchema
from app.presets.services import get_preset_by_code


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

    def get(self):
        '''Retrieve Message resource'''


        try:
            filter = self.get_argument("filter")
            filter_service = self.FILTER_SERVICES[filter]
        except:
            # Filter does not exist
            self.set_status(HTTPStatus.BAD_REQUEST)
            return self.finish()

        results = filter_service(self.tbh_user_id)
        # or to dump a list of objects
        message_schema = MessageSchema(many=True)
        results = {'messages': message_schema.dump(results).data }

        self.write(results)
        self.set_status(HTTPStatus.OK)
        self.finish()

    def post(self):
        '''Send message'''

        try:
            request_body = json_decode(self.request.body)
            receiver_phone_number = request_body['receiver_phone_number']
            message_text = get_preset_by_code(request_body['message_id'])
        except Exception as e:
            self.set_status(HTTPStatus.BAD_REQUEST)
            return self.finish()

        try:
            self.message_service.send_message(sender_id=self.tbh_user_id,
                receiver_phone_number=receiver_phone_number, text=message_text)
        except:
            self.set_status(HTTPStatus.UNAUTHORIZED)
            return self.finish()

        self.set_status(HTTPStatus.OK)
        self.finish()