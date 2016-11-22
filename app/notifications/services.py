from pyfcm import FCMNotification

from config import Config
from app.exceptions import PushNotifyError


NOTIFICATION_CONFIG = Config.PushNotifications
API_KEY = NOTIFICATION_CONFIG['api_key']


class PushNotifyService(object):
    def __init__(self, api_key):
        self.push_service = FCMNotification(api_key=API_KEY)

    @classmethod
    def from_config(cls):
        return cls(**NOTIFICATION_CONFIG)

    def send_push_notification(self, push_id, message_title, message_body):

        try:
            self.push_service.notify_single_device(registration_id=push_id,
              message_title=message_title, message_body=message_body)
        except:
            raise PushNotifyError('Error sending notification')