import sys

import psycopg2

from config import Config
from app.db import connections


def main():
    db_config = Config.postgres

    try:
        connections.reset(db_config['database'])
        sys.stdout.write('Creating environment successfully.\n')
    except psycopg2.Error:
        raise SystemExit('Could not connect to PostgreSQL.\n{0}'.format(sys.exc_info()))


if __name__ == '__main__':
    main()