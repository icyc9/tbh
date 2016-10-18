from app import init_application, sa_session_maker
import tornado.httpserver


application = init_application()
tornado.ioloop.IOLoop.instance().start()