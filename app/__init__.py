import os

import tornado.ioloop
import tornado.web
import tornado.options
import tornado.httpserver

from config import Config
from app.db.connections import create_sa_engine
from app.db.session import create_sa_session_maker
from app.tools.dotenv import set_env_file as _set_env


SERVER_PORT = Config.server_port
SERVER_HOST = Config.server_host
PROCESS_PER_CPU = Config.process_count
TORNADO_CONFIG = Config.Tornado

db_session = create_sa_engine()
sa_session_maker = create_sa_session_maker(db_session)


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

    ]

    make_server(
        handlers=handlers,
        port=SERVER_PORT,
        host=SERVER_HOST,
        tornado_config=TORNADO_CONFIG
    )

    tornado.ioloop.IOLoop.instance().start()