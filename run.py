from app import (main, start_development_server)
import tornado.httpserver


application = main()

if __name__ == '__main__':
    app = start_development_server()
    tornado.ioloop.IOLoop.instance().start()