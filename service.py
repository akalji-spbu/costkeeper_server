import api
import tornado.web
import tornado.httpserver

class PageOneHandler(tornado.web.RequestHandler):
    def get(self):
        vari = self.get_argument('vari', True)
        if(vari=="1"):
            self.write("hello  world")
        if (vari == "2"):
            self.write("hello cruel world")

class PageTwoHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("take some beer")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [('/pageone', PageOneHandler),
                ('/pagetwo', PageTwoHandler)]

        tornado.web.Application.__init__(self, handlers)

# Run the instance
application = Application()
http_server = tornado.httpserver.HTTPServer(application)
http_server.listen(14001)
tornado.ioloop.IOLoop.current().start()