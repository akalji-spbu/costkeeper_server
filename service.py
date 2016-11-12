import api
import tornado.web
import tornado.httpserver
import json

from tornado.options import define, options
define("port", default=14001, help="run on the given port", type=int)


class UserHandler(tornado.web.RequestHandler):
    def get(self):
        method = self.get_argument('method', True)


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


    def post(self):
        json_sting = self.request.body
        data_json = tornado.escape.json_decode(json_sting)
        method = str(data_json['type'])
        token  = str(data_json['token'])


        if (method == "user_reg"):
            text = data_json['object']['id']
            print(int(text))

        if (method == "user_auth"):
            login = self.get_argument('login', True)
            password = self.get_argument('password', True)
            token = api.user_auth(login, password)
            self.write(token)

        if (method == "user_alter"):
            print()

        if (method == "user_alter_password"):
            print()

        if (method == "user_delete"):
            print()



class ShopHandler(tornado.web.RequestHandler):
    def get(self):
        token = self.get_argument('token', True)
    def post(self):
        json_sting = self.request.body
        data_json = tornado.escape.json_decode(json_sting)
        method = str(data_json['type'])
        if (method == "shop_add"):
            print()

        if (method == "shop_alter"):
            print()

        if (method == "shop_complaint"):
            print()



class GoodHandler(tornado.web.RequestHandler):
    def get(self):
        token = self.get_argument('token', True)
    def post(self):
        json_sting = self.request.body
        data_json = tornado.escape.json_decode(json_sting)
        method = str(data_json['type'])
        if (method == "good_add"):
            print()

        if (method == "good_alter"):
            print()


class CostHandler(tornado.web.RequestHandler):
    def get(self):
        token = self.get_argument('token', True)
    def post(self):
        json_sting = self.request.body
        data_json = tornado.escape.json_decode(json_sting)
        method = str(data_json['type'])

        if (method == "cost_add"):
            print()


class BasketHandler(tornado.web.RequestHandler):
    def get(self):
        token = self.get_argument('token', True)
    def post(self):
        json_sting = self.request.body
        data_json = tornado.escape.json_decode(json_sting)
        method = str(data_json['type'])
        if (method == "basket_add"):
            print()

        if (method == "basket_add_item"):
            print()

        if (method == "basket_delete_item"):
            print()

        if (method == "basket_alter_item"):
            print()

        if (method == "basket_erase"):
            print()

        if (method == "basket_delete"):
            print()

        if (method == "basket_modify"):
            print()


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
http_server = tornado.httpserver.HTTPServer(application, xheaders=True)
http_server.listen(options.port)
tornado.ioloop.IOLoop.current().start()