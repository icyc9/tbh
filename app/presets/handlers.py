from app.base import BaseHandler
from app.auth.jwt import jwt_required
from app.presets.presets import MESSAGE_LIST


@jwt_required
class PresetHandler(BaseHandler):
    '''
    Base handler for the presets resource
    '''

    def get(self):
        self.write(MESSAGE_LIST)
        self.finish()