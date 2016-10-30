from sqlalchemy import (Column, Integer, BigInteger,
                        String, ForeignKey)

from app import db_base


class Message(db_base):
    __tablename__ = 'message'

    sender_id = Column(BigInteger, ForeignKey('tbh_user.id'), primary_key=True)
    receiver_id = Column(BigInteger, ForeignKey('tbh_user.id'), primary_key=True)
    text = Column(String(50, convert_unicode=True))
    status = Column(Integer)