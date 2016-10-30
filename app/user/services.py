from sqlalchemy.orm.exc import NoResultFound

from app.exceptions import ResourceError


class UserAccountService:
    '''
    Service for user account creation and manipulation
    '''

    def __init__(self, user_repository):
        self.user_repository = user_repository

    def create_pending_user(self, phone_number):
        '''
        Adds a pending invited user to the database.
        '''

        return self.user_repository.create_pending_user(phone_number=phone_number)

    def create_verified_user(self, user_id, phone_number, gender):
        '''
        Adds a verified user account to the database.
        '''

        return self.user_repository.create_verified_user(
            user_id=user_id, phone_number=phone_number, gender=gender)

    def verify_user(self, phone_number):
        '''
        Changes user account status to verified
        '''

        self.user_repository.verify_user(phone_number=phone_number)

    def retrieve_user_by_id(self, user_id):
        '''
        Retrieve a user from the database
        '''

        self.user_repository.get_user_by_id(user_id=user_id)

    def verify_user_resource(self, user_id, phone_number, gender):
        '''
        Set a users status as verified.
        If the resource does not exist, create a verified user.
        '''

        try:
            # Verify the user status
            self.user_repository.verify_user(phone_number=phone_number)
        except (ResourceError, NoResultFound):
            # The user does not exist
            # Create the user
            self.user_repository.create_verified_user(
                user_id=user_id, phone_number=phone_number, gender=gender)

    def retrieve_user_by_phone_number(self, phone_number):
        '''
        Retrieve a user from the database
        '''

        return self.user_repository.get_user_by_phone_number(phone_number=phone_number)
