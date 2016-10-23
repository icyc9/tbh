from sqlalchemy.ext.declarative import (declarative_base, declared_attr)
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
import sqlalchemy as sa


mymetadata = sa.MetaData()
Base = declarative_base(metadata=mymetadata)


class MessageBaseMixin(object):

    @declared_attr
    def sender_id(self):
        return Column(Integer, ForeignKey('users.id'), primary_key=True)

    @declared_attr
    def receiver_id(self):
        return Column(Integer, ForeignKey('users.id'), primary_key=True)

    text = Column(String(50))


class PendingMessages(MessageBaseMixin, Base):
    __tablename__ = 'received_messages'


class NeutralMessage(MessageBaseMixin, Base):
    __tablename__ = 'neutral_message'


class UserBaseMixin(object):


class User(Base):

    @declared_attr
    def id(self):
        return Column(Integer, primary_key=True)

    @declared_attr
    def username(self):
        return Column(String(40))



    __tablename__ = 'users'

    received_pending_messages = relationship(
        'PendingMessages',
        foreign_keys='PendingMessages.receiver_id',
        backref='receiving_user'
    )

    sent_pending_messages = relationship(
        'PendingMessages',
        foreign_keys='PendingMessages.sender_id',
        backref='sending_user'
    )

    received_mutual_messages = relationship(
        'NeutralMessage',
        foreign_keys='NeutralMessage.receiver_id',
        backref='receiving_user'
    )

    sent_mutual_messages = relationship(
        'NeutralMessage',
        foreign_keys='NeutralMessage.sender_id',
        backref='sending_user'
    )