import sqlalchemy

from app.exceptions import (ResourceError, DuplicateMessage)


PENDING_MESSAGE_STATUS = 0
MUTUAL_MESSAGE_STATUS = 1


class MessageService(object):

    '''
    Message service
    '''

    def __init__(self, user_service, message_repository, push_notify_service):
        self.user_service = user_service
        self.message_repository = message_repository
        self.push_notify_service = push_notify_service

    def send_message(self, sender_id, receiver_phone_number, text):
        users = self.message_repository.get_sender_and_receiver(
            sender_id=sender_id, receiver_phone_number=receiver_phone_number)

        try:
            # Filter query results and label sender
            sending_user = [user for user in users if user.id == sender_id][0]
        except IndexError:
            raise ResourceError(reason='Sending user does not exist', status=409)

        try:
            # Filter query results and label receiver
            receiver = [user for user in users if not user.id == sender_id][0]
        except IndexError:
            # Receiving user does not exist
            # Create a pending user
            receiver = self.user_service.create_pending_user(
                phone_number=receiver_phone_number)

        sender_push_id = sending_user.push_id
        receiver_push_id = receiver.push_id
        sender_gender = 'guy' if sending_user.gender == 0 else 'girl'
        receiver_gender = 'guy' if receiver.gender == 0 else 'girl'

        try:
            pending_messages = self.message_repository.\
                get_pending_messages_between_users(sender_id=sender_id,receiver_id=receiver.id, text=text)

            if pending_messages.sender_id == sender_id:
                # Sender has already sent this
                raise DuplicateMessage(reason='Sender has already sent this message', status=409)

            self.message_repository.delete_messages(messages=pending_messages)
            self.message_repository.create_message(sending_user=sending_user, receiving_user=receiver,
                                                   text=text, status=MUTUAL_MESSAGE_STATUS)

            self.push_notify_service.send_push_notification(push_id=sender_push_id,
                message_title='New match!', message_body='You are matched with a %s' % sender_gender)

            self.push_notify_service.send_push_notification(push_id=receiver_push_id,
                message_title='New match!', message_body='You are matched with a %s' % receiver_gender)

        except sqlalchemy.orm.exc.NoResultFound:
            # Pending message does not exist between the users
            # Create a pending message
            self.message_repository.create_message(sending_user=sending_user, receiving_user=receiver,
                                                   text=text, status=PENDING_MESSAGE_STATUS)

            self.push_notify_service.send_push_notification(push_id=receiver_push_id,
                message_title='Message received!', message_body='New anonymous message')

    def get_received_messages(self, user_id):
        return self.message_repository.get_received_messages(user_id=user_id)

    def get_sent_messages(self, user_id):
        return self.message_repository.get_sent_messages(user_id=user_id)

    def get_mutual_messages(self, user_id):
        mutual_messages = self.message_repository.get_mutual_messages(user_id=user_id)
        messages = []

        for message in mutual_messages:
            sender = message.sending_user
            receiver = message.receiving_user

            user = sender if sender.id != user_id else receiver
            current_message = {'sender': user, 'text': message.text}

            messages.append(current_message)

        return messages
