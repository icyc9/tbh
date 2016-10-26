import os
import ast

from app.tools.dotenv import set_env_file as _set_env


_set_env(os.path.join(os.path.dirname(__file__), '.env'))


class Config(object):

    server_port = int(os.environ['PORT'])
    process_count = int(os.environ['PROCESS_COUNT'])
    server_host = os.environ['SERVER_HOST']

    JWT = {
        'secret': os.environ['JWT_SECRET']
    }

    Tornado = {
        'autoreload': ast.literal_eval(os.environ['AUTORELOAD']),
        'debug': ast.literal_eval(os.environ['DEBUG'])
    }

    postgres = {
        'host': os.environ['DB_HOST'],
        'database': os.environ['DB'],
        'user': os.environ['DB_USER'],
        'password': os.environ['DB_PASSWORD']
    }
