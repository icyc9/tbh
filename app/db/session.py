from contextlib import contextmanager

from sqlalchemy.orm import sessionmaker


@contextmanager
def sa_session(Session):
    """Provide a transactional scope around a series of operations."""

    session = Session()
    session.expire_on_commit = False

    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def create_sa_session_maker(engine):
    '''
    Create and bind a SQL Alchemy Session maker to an engine
    '''

    Session = sessionmaker(bind=engine)

    return Session


def create_sa_session(session_maker):
    '''
    Create a pg session for interaction with the db
    '''

    return session_maker()