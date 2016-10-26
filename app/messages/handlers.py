
import json

import jwt

from app.base import BaseHandler
from app.auth.jwt import jwt_required


@jwt_required
class MessageHandler(BaseHandler):
    '''
    Base handler for the message resource
    '''

    '''Retrieve Message resource'''
    def get(self):
        self.write(json.dumps({'user_id': self.tbh_user_id})
        self.set_header('Content-Type', 'application/json')
