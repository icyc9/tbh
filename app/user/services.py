from sqlalchemy.orm.exc import NoResultFound

from app.db.session import sa_session
from app.exceptions import ResourceError
from app.user.models import TBHUser


class UserAccountService:
    '''
    Service for user account creation and manipulation
    '''

    def __init__(self, sa_session_maker):
        self.sa_session_maker = sa_session_maker

    def create_pending_user(self, phone_number):
        '''
        Adds a pending invited user to the database.
        '''

        with sa_session(self.sa_session_maker) as session:
            invited_user = TBHUser(phone_number=phone_number, status=0)
            session.add(invited_user)

        return invited_user

    @staticmethod
    def create_verified_user(session, user_id, phone_number, gender):
        '''
        Adds a verified user account to the database.
        '''

        invited_user = TBHUser(id=user_id, phone_number=phone_number, status=1, gender=gender)
        session.add(invited_user)

    @staticmethod
    def verify_user(session, phone_number):
        '''
        Changes user account status to verified
        '''

        user = session.query(TBHUser).filter(
            TBHUser.phone_number == phone_number).one()

        if not user:
            raise ResourceError('User resource not found')

        user.status = 1

    @staticmethod
    def retrieve_user_by_id(session, user_id):
        '''
        Retrieve a user from the database
        '''

        user = session.query(TBHUser).filter(TBHUser.id == user_id).one()

        if not user:
            raise ResourceError('User resource not found')

        return user

    def verify_user_resource(self, user_id, phone_number, gender):
        '''
        Set a users status as verified.
        If the resource does not exist, create a verified user.
        '''
        with sa_session(self.sa_session_maker) as session:

            try:
                # Verify the user status
                self.verify_user(session=session, phone_number=phone_number)
            except (ResourceError, NoResultFound):
                # The user does not exist
                # Create the user
                self.create_verified_user(session=session,
                    user_id=user_id, phone_number=phone_number, gender=gender)

    @staticmethod
    def retrieve_user_by_phone_number(session, phone_number):
        '''
        Retrieve a user from the database
        '''

        user = session.query(TBHUser).filter(
            TBHUser.phone_number == phone_number).one()

        if not user:
            raise ResourceError('User resource not found')

        return user

