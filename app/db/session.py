from contextlib import contextmanager

from sqlalchemy.orm import (scoped_session, sessionmaker, sessionmaker)


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


def create_sa_session_maker(engine, **kwargs):
    '''
    Create and bind a SQL Alchemy Session maker to an engine
    '''

    Session = sessionmaker(bind=engine, **kwargs)

    return Session


def create_sa_session(session_maker):
    '''
    Create a pg session for interaction with the db
    '''

    return session_maker()


def create_scoped_session(engine, **kwargs):
    '''
    Create a scoped sesion
    '''

    return scoped_session(create_sa_session_maker(engine, **kwargs))
