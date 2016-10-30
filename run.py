from app import init_application
import tornado.httpserver


application = init_application()
tornado.ioloop.IOLoop.instance().start()