import os
from http import HTTPStatus

import tornado.web
import tornado.ioloop
import tornado.web
import tornado.options
import tornado.httpserver
import tornado.wsgi
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

from app.db.connections import create_sa_engine
from app.db.session import create_sa_session_maker
from app.tools.dotenv import set_env_file as _set_env
from app.db.session import create_scoped_session
from app.db.base import Database as BaseDB
from app.auth.services import (AuthService, JWTService)
from app.user.services import UserAccountService
from app.messages.services import MessageService
from app.notifications.services import PushNotifyService
from app.auth.handlers import AuthHandler
from app.messages.handlers import MessageHandler
from app.presets.handlers import PresetHandler
from app.base import BaseHandler
from config import Config


SERVER_PORT = Config.server_port
SERVER_HOST = Config.server_host
PROCESS_PER_CPU = Config.process_count
TORNADO_CONFIG = Config.Tornado


class Database(BaseDB):
    def __init__(self):
        self.engine = create_sa_engine()
        self.scoped_session = create_scoped_session(self.engine)
        self.metadata = sa.MetaData()
        self.base = declarative_base(metadata=self.metadata)

    def get_engine(self):
        return self.engine

    def get_scoped_session(self):
        return self.scoped_session

    def get_metadata(self):
        return self.metadata

    def get_declaractive_base(self):
        return self.base


database = Database()

from app.user.models import *
from app.messages.models import *
from app.user.repository import UserRepository
from app.messages.repository import MessageRepository

user_repository = UserRepository(database=database)
message_repository = MessageRepository(database=database)

auth_service = AuthService()
jwt_service = JWTService()
push_notify_service = PushNotifyService.from_config()
user_service = UserAccountService(user_repository=user_repository)
message_service = MessageService(user_service=user_service,
                                 message_repository=message_repository,
                                 push_notify_service=push_notify_service)

__version__ = '0.0.1'

_set_env(os.path.join(
    os.path.dirname(os.path.dirname(__file__)), '.env'))


class BaseHandler(BaseHandler):
    def get(self):
        self.set_status(int(HTTPStatus.OK))
        self.finish()


class Application(tornado.web.Application):
    def __init__(self, tornado_config):
        self.database = database
        self.db_metadata = self.database.get_metadata()
        self.db_engine = self.database.get_engine()
        self.scoped_session = self.database.get_scoped_session()

        handlers = [
            ('/', BaseHandler),
            ('/auth', AuthHandler, dict(
                auth_service=auth_service,
                user_account_service=user_service,
                jwt_service=jwt_service)
             ),

            ('/messages', MessageHandler, dict(
                message_service=message_service)
             ),

            ('/presets', PresetHandler)
        ]

        tornado.web.Application.__init__(self, handlers, **tornado_config)

    def get_database(self):
        return self.database

    def create_tables(self, **kwargs):
        self.db_metadata.create_all(bind=self.db_engine, **kwargs)

    def drop_tables(self, **kwargs):
        self.db_metadata.drop_all(bind=self.db_engine, **kwargs)

    def start_server(self, port, address, num_processes):
        server = tornado.httpserver.HTTPServer(self)
        server.bind(port=port, address=address)
        server.start(num_processes=num_processes)


def main(*args):
    tornado_app = Application(tornado_config=TORNADO_CONFIG)
    application = tornado.wsgi.WSGIAdapter(tornado_app)

    return application


def start_development_server():
    tornado_app = Application(tornado_config=TORNADO_CONFIG)
    tornado_app.start_server(port=SERVER_PORT, address=SERVER_HOST,
                             num_processes=PROCESS_PER_CPU)

    return tornado_app