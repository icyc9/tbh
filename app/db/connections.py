import psycopg2
import sqlalchemy as sa

from app.db.base import Database
from config import Config


def reset(db_name):
    """Reset database."""

    conn = psycopg2.connect(database='postgres')
    db = Database(db_name)
    conn.autocommit = True

    with conn.cursor() as cursor:
        cursor.execute(db.drop_statement())
        cursor.execute(db.create_statement())
    conn.close()


def create_sa_engine(host=None, database=None, user=None, password=None,
                     **kwargs):
    """Sqlalchemy engine."""

    host = host or Config.postgres['host']
    database = database or Config.postgres['database']
    user = user or Config.postgres['user']
    password = password or Config.postgres['password']



    sa_url = format_sa_url(host=host, database=database,
                           user=user, password=password)
    return sa.create_engine(sa_url, **kwargs)


def format_sa_url(host, database, user, password):
    """Format psycopg2 connection parameters to Sqlalchemy engine."""

    sa_url = sa.engine.url.URL('postgresql', host=host, database=database,
                               username=user, password=password)
    return sa_url