from contextlib import contextmanager

from sqlalchemy import (or_, and_)

from app.db.session import sa_session
from app.messages.models import Message
from app.user.models import TBHUser


PENDING_MESSAGE_STATUS = 0
MUTUAL_MESSAGE_STATUS = 1


class MessageRepository(object):

    '''
    Repository layer for messages
    '''

    @staticmethod
    def create_message(session, sending_user, receiving_user, text, status):
        '''
        Create a message instance
        '''

        message = Message(sending_user=sending_user,
                          receiving_user=receiving_user,
                          text=text, status=status)

        session.add(message)

    @staticmethod
    def get_sender_and_receiver(session, sender_id, receiver_phone_number):
        '''
        Get a sender by id, and receiver by phone number in a single query.
        '''

        users = session.query(TBHUser) \
            .filter(or_(TBHUser.id == sender_id,
                        TBHUser.phone_number == receiver_phone_number)).all()

        return users

    @staticmethod
    def get_pending_messages_between_users(session, sender_id, receiver_id, text):
        '''
        Get all pending messages between two users
        '''

        pending_messages = session.query(Message) \
            .filter(and_(
                (Message.sender_id == sender_id) |
                (Message.sender_id == receiver_id),
                (Message.text == text))).one()

        return pending_messages

    @staticmethod
    def get_received_messages(session, user_id):
        '''
        Get all received messages of a user
        '''

        received_messages = session.query(Message) \
            .filter(and_(Message.receiver_id == user_id,
                         Message.status == PENDING_MESSAGE_STATUS)).all()

        return received_messages

    @staticmethod
    def get_sent_messages(session, user_id):
        '''
        Get all messages sent by a user
        '''

        sent_messages = session.query(Message) \
            .filter(and_(Message.sender_id == user_id,
                         Message.status == PENDING_MESSAGE_STATUS)).all()

        return sent_messages

    @staticmethod
    def get_mutual_messages(session, user_id):
        '''
        Get all mutual messages for a user
        '''

        mutual_messages = session.query(Message) \
            .filter(and_(
                ((Message.sender_id == user_id) |
                (Message.receiver_id == user_id)),
                ((Message.status == MUTUAL_MESSAGE_STATUS))
            )).all()

        return mutual_messages