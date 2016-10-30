import base64

from sqlalchemy import (or_, and_)
from sqlalchemy.orm.exc import NoResultFound

from app.db.session import sa_session
from app.messages.models import Message
from app.user.models import TBHUser


PENDING_MESSAGE_STATUS = 0
MUTUAL_MESSAGE_STATUS = 1


class MessageService(object):

    '''
    Message service
    '''

    def __init__(self, sa_session_maker, account_service):
        self._sa_session_maker = sa_session_maker
        self.account_service = account_service

    def send_message(self, sender_id, receiver_phone_number, text):
        with sa_session(self._sa_session_maker) as session:
            # Retrieve sending and receiving user in one query
            users = session.query(TBHUser) \
                .filter(or_(TBHUser.id == sender_id,
                    TBHUser.phone_number == receiver_phone_number)).all()

            # Filter query results and label users
            try:
                sending_user = [user for user in users if user.id == sender_id][0]
            except IndexError:
                raise ValueError('Sending user does not exist')

            try:
                receiving_user = [user for user in users if not user.id == sender_id][0]
            except IndexError:
                # Receiving user does not exist
                # Create a pending user
                invited_user = TBHUser(phone_number=receiver_phone_number, status=0)
                session.add(invited_user)

            try:
                # Search for any pending messages between the two users
                pending_messages = session.query(Message) \
                    .filter(and_(
                        (Message.sender_id == sender_id) |
                        (Message.sender_id == invited_user.id),
                        (Message.text == text))).one()

                # Pending message of this type was found - delete it
                session.delete(pending_messages)
                # Create a mutual message
                Message(sending_user=sending_user, receiving_user=invited_user, text=text, status=1)
            except NoResultFound:
                # Pending message does not exist between the users
                # Create a pending message
                Message(sending_user=sending_user, receiving_user=invited_user, text=text, status=0)

    def get_received_messages(self, user_id):
        with sa_session(self._sa_session_maker) as session:
            received_messages = session.query(Message) \
                .filter(and_(Message.receiver_id == user_id,
                             Message.status == PENDING_MESSAGE_STATUS)).all()

            return received_messages

    def get_sent_messages(self, user_id):
        with sa_session(self._sa_session_maker) as session:
            sent_messages = session.query(Message) \
                .filter(and_(Message.sender_id == user_id,
                             Message.status == PENDING_MESSAGE_STATUS)).all()

            return sent_messages

    def get_mutual_messages(self, user_id):
        with sa_session(self._sa_session_maker) as session:
            mutual_messages = session.query(Message) \
                .filter(and_(
                    ((Message.sender_id == user_id) |
                    (Message.receiver_id == user_id)),
                    ((Message.status == MUTUAL_MESSAGE_STATUS))
                )).all()

            return mutual_messages