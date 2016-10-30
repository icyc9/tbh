from sqlalchemy import (Column, Integer, BigInteger,
                        String, ForeignKey)

from app import database


Base = database.get_declaractive_base()


class Message(Base):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True)
    sender_id = Column(BigInteger, ForeignKey('tbh_user.id'))
    receiver_id = Column(BigInteger, ForeignKey('tbh_user.id'))
    text = Column(String(50, convert_unicode=True))
    status = Column(Integer)