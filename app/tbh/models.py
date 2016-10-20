from sqlalchemy.ext.declarative import (declarative_base, declared_attr)
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import Column, Integer, String, ForeignKey, Table, UniqueConstraint, Sequence
from sqlalchemy.orm import relationship, backref
import sqlalchemy as sa

from app import db_session


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


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
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

    received_neutral_message = relationship(
        'NeutralMessage',
        foreign_keys='NeutralMessage.receiver_id',
        backref='receiving_user'
    )

    sent_neutral_messages = relationship(
        'NeutralMessage',
        foreign_keys='NeutralMessage.sender_id',
        backref='sending_user'
    )