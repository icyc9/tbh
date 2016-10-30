from sqlalchemy import Column, Integer, BigInteger, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types.phone_number import PhoneNumberType

from app import database
from app.messages.models import Message


Base = database.get_declaractive_base()


class TBHUser(Base):
    __tablename__ = 'tbh_user'


    id = Column(BigInteger, primary_key=True)
    phone_number = Column(PhoneNumberType())
    type = Column(String(50))
    status = Column(Integer)
    gender = Column(Integer)

    sent_pending_messages = relationship(
        'Message',
        foreign_keys='Message.sender_id',
        backref='sending_user',
        lazy="dynamic",
    )

    received_pending_messages = relationship(
        'Message',
        foreign_keys='Message.receiver_id',
        backref='receiving_user',
        lazy="dynamic"
    )


    def is_verified(self):
        return self.status == 1

    def is_pending(self):
        return self.status == 0

    def is_male(self):
        return self.gender == 0

    def is_female(self):
        return self.gender == 1