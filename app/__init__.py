import os

import tornado.ioloop
import tornado.web
import tornado.options
import tornado.httpserver
import sqlalchemy as sa
from sqlalchemy.ext.declarative import (declarative_base, declared_attr)

from app.db.connections import create_sa_engine
from app.db.session import create_sa_session_maker
from app.tools.dotenv import set_env_file as _set_env
from config import Config


SERVER_PORT = Config.server_port
SERVER_HOST = Config.server_host
PROCESS_PER_CPU = Config.process_count
TORNADO_CONFIG = Config.Tornado


db_session = create_sa_engine()
sa_session_maker = create_sa_session_maker(db_session)
db_metadata = sa.MetaData()
db_base = declarative_base(metadata=db_metadata)

from app.auth.handlers import AuthHandler
from app.messages.handlers import MessageHandler
from app.presets.handlers import PresetHandler

from app.user.models import *
from app.messages.models import *

from app.auth.services import (AuthService, JWTService)
from app.user.services import UserAccountService
from app.messages.services import MessageService

auth_service = AuthService()
user_account_service = UserAccountService(sa_session_maker)
jwt_service = JWTService()
message_service = MessageService(sa_session_maker, user_account_service)

__version__ = '0.0.1'

_set_env(os.path.join(
    os.path.dirname(os.path.dirname(__file__)), '.env'))


def make_server(handlers, port, host, tornado_config):
    app = tornado.web.Application(handlers, **tornado_config)

    server = tornado.httpserver.HTTPServer(app)
    server.bind(port=port, address=host)
    server.start(0)

    return app


def init_application():


    handlers = [
        ('/auth', AuthHandler, dict(
            auth_service=auth_service,
            user_account_service=user_account_service,
            jwt_service=jwt_service
        )),
        ('/messages', MessageHandler, dict(
            message_service=message_service
        )),
        ('/presets', PresetHandler)
    ]

    make_server(
        handlers=handlers,
        port=SERVER_PORT,
        host=SERVER_HOST,
        tornado_config=TORNADO_CONFIG
    )


db_metadata.drop_all(db_session)
db_metadata.create_all(db_session)