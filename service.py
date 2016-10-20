import api
import tornado.web
import tornado.httpserver
import json

class PageOneHandler(tornado.web.RequestHandler):
    def get(self):
        token = self.get_argument('token', True)
        if(token=="Qwerty12345"):
           req = self.get_argument('req', True)
           self.write(req)
        else:
            self.write("Bye")

class UserHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Bye")
        method = self.get_argument('method', True)
        if(method=="reg"):
            login       = self.get_argument('login', True)
            email       = self.get_argument('email', True)
            password    = self.get_argument('password', True)
            api.user_reg(login,email,password)


        if(method=="auth"):
            login       = self.get_argument('login', True)
            password    = self.get_argument('password', True)
            token       = api.user_auth(login,password)
            self.write(token)
        else:
            token = self.get_argument('token', True)
            UID = api.user_check_token(token)
            if (token == "Qwerty12345"):
                answer = api.UsersMethods(self.get_argument('method', True), self.get_argument('req', True))


class ShopHandler(tornado.web.RequestHandler):
    def get(self):
        token = self.get_argument('token', True)
    def post(self):
        token = self.get_argument('token', True)


class GoodHandler(tornado.web.RequestHandler):
    def get(self):
        token = self.get_argument('token', True)
    def post(self):
        token = self.get_argument('token', True)


class CostHandler(tornado.web.RequestHandler):
    def get(self):
        token = self.get_argument('token', True)
    def post(self):
        token = self.get_argument('token', True)


class BasketHandler(tornado.web.RequestHandler):
    def get(self):
        token = self.get_argument('token', True)
    def post(self):
        token = self.get_argument('token', True)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [('/user',   UserHandler),
                    ('/shop',   ShopHandler),
                    ('/good',   GoodHandler),
                    ('/cost',   CostHandler),
                    ('/basket', BasketHandler)]
        tornado.web.Application.__init__(self, handlers)


# Run the instance
application = Application()
http_server = tornado.httpserver.HTTPServer(application)
http_server.listen(14001)
tornado.ioloop.IOLoop.current().start()