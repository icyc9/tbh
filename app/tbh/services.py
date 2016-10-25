from app.db.session import sa_session
from app import sa_session_maker, db_session
from app.tbh.models import TBHUser, PendingMessages, InvitedUser, VerifiedUser


def create_user_invitation(id, phone_number):
    '''
    Adds a pending invited user to the database.

    The InvitedUser table temporarily holds users that have
    been invited and have not completed the sign up process.

    An invited user is persisted in the TBHUser
    Table upon the invited user signing up.
    '''

    with sa_session(sa_session_maker) as session:
        invited_user = InvitedUser(
            id=id, phone_number=phone_number)

        session.add(invited_user)


def delete_user_invitation(invited_user):
    '''
    Remove a user invitation from the database
    '''

    with sa_session(sa_session_maker) as session:
        session.delete(invited_user)


def create_verified_user(id, phone_number):
    '''
    Add a verified user to the database.
    A verified user has successfully completed the signup
    process ofered through Digits.
    '''


    with sa_session(sa_session_maker) as session:
        verified_user = VerifiedUser(
            id=id, phone_number=phone_number)

        session.add(verified_user)


def upgrade_user_account(id):
    '''
    Upgrade from an InvitedUser to a VerifiedUser
    '''

    pass