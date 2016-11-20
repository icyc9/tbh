from app.user.models import TBHUser
from app.db.session import sa_session
from app.exceptions import ResourceError


PENDING_STATUS = 0
VERIFIED_STATUS = 1


class UserRepository(object):
    def __init__(self, database):
        self.scoped_session = database.get_scoped_session()

    def create_pending_user(self, phone_number):
        with sa_session(self.scoped_session) as session:
            invited_user = TBHUser(phone_number=phone_number,
                                   status=PENDING_STATUS)
            session.add(invited_user)

            return invited_user

    def create_verified_user(self, user_id, phone_number, gender, push_id):
        with sa_session(self.scoped_session) as session:
            invited_user = TBHUser(phone_number=phone_number, id=user_id,
                                   status=VERIFIED_STATUS, gender=gender, push_id=push_id)
            session.add(invited_user)

            return invited_user

    def verify_user(self, phone_number):
        with sa_session(self.scoped_session) as session:

            try:
                user = session.query(TBHUser).filter(
                    TBHUser.phone_number == phone_number).one()
            except:
                raise ResourceError('User resource not found')

            user.status = 1

    def get_user_by_id(self, user_id):
        with sa_session(self.scoped_session) as session:
            try:
                user = session.query(TBHUser).filter(TBHUser.id == user_id).one()
            except:
                raise ResourceError('User resource not found')

            return user

    def get_user_by_phone_number(self, phone_number):
        with sa_session(self.scoped_session) as session:
            try:
                user = session.query(TBHUser) \
                    .filter(TBHUser.get_user_by_phone_number ==
                            phone_number).one()
            except:
                raise ResourceError('User resource not found')

            return user