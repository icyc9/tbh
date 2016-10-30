from sqlalchemy.orm.exc import NoResultFound

from app.exceptions import (ResourceError, DuplicateMessage)


PENDING_MESSAGE_STATUS = 0
MUTUAL_MESSAGE_STATUS = 1


class MessageService(object):

    '''
    Message service
    '''

    def __init__(self, user_service, message_repository):
        self.user_service = user_service
        self.message_repository = message_repository

    def send_message(self, sender_id, receiver_phone_number, text):
        users = self.message_repository.get_sender_and_receiver(
            sender_id=sender_id, receiver_phone_number=receiver_phone_number)

        try:
            # Filter query results and label sender
            sending_user = [user for user in users if user.id == sender_id][0]
        except IndexError:
            raise ResourceError('Sending user does not exist')

        try:
            # Filter query results and label receiver
            receiver = [user for user in users if not user.id == sender_id][0]
        except IndexError:
            # Receiving user does not exist
            # Create a pending user
            receiver = self.user_service.create_pending_user(
                phone_number=receiver_phone_number)

        try:
            pending_messages = self.message_repository.\
                get_pending_messages_between_users(sender_id=sender_id,receiver_id=receiver.id, text=text)

            if pending_messages.sender_id == sender_id:
                # Sender has already sent this
                raise DuplicateMessage('Sender has already sent this message')

            self.message_repository.delete_messages(messages=pending_messages)
            self.message_repository.create_message(sending_user=sending_user, receiving_user=receiver,
                                                   text=text, status=MUTUAL_MESSAGE_STATUS)
        except NoResultFound:
            # Pending message does not exist between the users
            # Create a pending message
            self.message_repository.create_message(sending_user=sending_user, receiving_user=receiver,
                                                   text=text, status=PENDING_MESSAGE_STATUS)

    def get_received_messages(self, user_id):
        return self.message_repository.get_received_messages(user_id=user_id)

    def get_sent_messages(self, user_id):
        return self.message_repository.get_sent_messages(user_id=user_id)

    def get_mutual_messages(self, user_id):
        return self.message_repository.get_mutual_messages(user_id=user_id)