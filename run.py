from app import main
import tornado.httpserver


application = main()
tornado.ioloop.IOLoop.instance().start()