from sqlalchemy.ext.declarative import (declarative_base, declared_attr)
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types.phone_number import PhoneNumberType
import sqlalchemy as sa

from app import db_session

mymetadata = sa.MetaData()
Base = declarative_base(metadata=mymetadata)


class MessageBaseMixin(object):
    @declared_attr
    def sender_id(self):
        return Column(Integer, ForeignKey('tbh_user.id'), primary_key=True)


    @declared_attr
    def receiver_id(self):
        return Column(Integer, ForeignKey('tbh_user.id'), primary_key=True)

    text = Column(String(50))


class PendingMessages(MessageBaseMixin, Base):
    __tablename__ = 'received_messages'


class MutualMessage(MessageBaseMixin, Base):
    __tablename__ = 'mutual_message'


class TBHUser(Base):
    __tablename__ = 'tbh_user'


    id = Column(Integer, primary_key=True)
    username = Column(String(40))
    phone_number = Column(PhoneNumberType())
    type = Column(String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'tbh_user',
        'polymorphic_on': type
    }

    sent_pending_messages = relationship(
        'PendingMessages',
        foreign_keys='PendingMessages.sender_id',
        backref='sending_user'
    )

    sent_mutual_messages = relationship(
        'MutualMessage',
        foreign_keys='MutualMessage.sender_id',
        backref='sending_user'
    )

    received_mutual_messages = relationship(
        'MutualMessage',
        foreign_keys='MutualMessage.receiver_id',
        backref='receiving_user'
    )

    received_pending_messages = relationship(
        'PendingMessages',
        foreign_keys='PendingMessages.receiver_id',
        backref='receiving_user'
    )


class InvitedUser(TBHUser):
    __tablename__ = 'invited_user'
    id = Column(Integer, ForeignKey('tbh_user.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'invited_user',
    }


class VerifiedUser(TBHUser):
    __tablename__ = 'verified_user'
    id = Column(Integer, ForeignKey('tbh_user.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'verified_user',
    }