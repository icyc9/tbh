from sqlalchemy import (or_, and_)

from app.messages.models import Message
from app.user.models import TBHUser
from app.db.session import sa_session


PENDING_MESSAGE_STATUS = 0
MUTUAL_MESSAGE_STATUS = 1


class MessageRepository(object):

    '''
    Repository layer for messages
    '''

    def __init__(self, database):
        self.scoped_session = database.get_scoped_session()

    def create_message(self, sending_user, receiving_user, text, status):
        '''
        Create a message instance
        '''

        with sa_session(self.scoped_session) as session:
            message = Message(sending_user=sending_user,
                              receiving_user=receiving_user,
                              text=text, status=status)

            session.add(message)

    def get_sender_and_receiver(self, sender_id, receiver_phone_number):
        '''
        Get a sender by id, and receiver by phone number in a single query.
        '''

        with sa_session(self.scoped_session) as session:
            users = session.query(TBHUser) \
                .filter(or_(TBHUser.id == sender_id,
                            TBHUser.phone_number == receiver_phone_number)).all()

            return users

    def get_pending_messages_between_users(self, sender_id, receiver_id, text):
        '''
        Get all pending messages between two users
        '''

        with sa_session(self.scoped_session) as session:
            pending_messages = session.query(Message) \
                .filter(and_(
                    (Message.sender_id == sender_id) |
                    (Message.sender_id == receiver_id),
                    (Message.text == text)))\
                .filter(Message.receiver_id == receiver_id).one()

            return pending_messages

    def get_received_messages(self, user_id):
        '''
        Get all received messages of a user
        '''

        with sa_session(self.scoped_session) as session:
            received_messages = session.query(Message) \
                .filter(and_(Message.receiver_id == user_id,
                             Message.status == PENDING_MESSAGE_STATUS)).all()

            return received_messages

    def get_sent_messages(self, user_id):
        '''
        Get all messages sent by a user
        '''

        with sa_session(self.scoped_session) as session:
            sent_messages = session.query(Message) \
                .filter(and_(Message.sender_id == user_id,
                             Message.status == PENDING_MESSAGE_STATUS)).all()

            return sent_messages

    def get_mutual_messages(self, user_id):
        '''
        Get all mutual messages for a user
        '''

        with sa_session(self.scoped_session) as session:
            mutual_messages = session.query(Message) \
                .filter(and_(
                    ((Message.sender_id == user_id) |
                    (Message.receiver_id == user_id)),
                    ((Message.status == MUTUAL_MESSAGE_STATUS))
                )).all()

            return mutual_messages

    def delete_messages(self, messages):
        with sa_session(self.scoped_session) as session:
            session.delete(messages)