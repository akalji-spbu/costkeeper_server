import api
import tornado.web
import tornado.httpserver
import json

from tornado.options import define, options
define("port", default=14001, help="run on the given port", type=int)


class UserHandler(tornado.web.RequestHandler):
    def get(self):
        method = self.get_argument('method', True)
        if (method == "user_get"):
            token = self.get_argument('token', True)
            ID = self.get_argument('user_id', True)
            secret = self.get_argument('secret', True)
            self.write(api.user_get(token, ID, secret))

    def post(self):
        json_sting = self.request.body
        data_json = tornado.escape.json_decode(json_sting)
        method = str(data_json['type'])
        token  = str(data_json['token'])
        secret = str(data_json['secret'])
        object = data_json['object']


        if (method == "user_reg"):
            nickname    = str(object['nickname'])
            password    = str(object['password'])
            email       = str(object['email'])
            firstname   = str(object['firstname'])
            lastname    = str(object['lastname'])
            avatar      = str(object['avatar'])
            nickname_exist,email_exist = api.check_username_and_email(nickname, email)
            if(nickname_exist == False and email_exist == False):
                reg = api.user_reg(nickname, password, email, firstname, lastname, avatar)
                if (reg == True):
                    self.write("Success")
            else:
                if(nickname_exist == True):
                    self.write("NICKNAME_IS_USED\n")
                if (email_exist == True):
                    self.write("EMAIL_IS_USED\n")

        if (method == "user_auth"):
            email    = str(object['email'])
            password = str(object['password'])
            status, token = api.user_auth(email, password)
            if (status == True):
                self.write(token)
            else:
                self.write("UserDoesNotExist")


        if (method == "user_alter"):
            nickname    = str(object['nickname'])
            email       = str(object['email'])
            firstname   = str(object['firstname'])
            lastname    = str(object['lastname'])
            avatar      = str(object['avatar'])
            self.write(api.user_alter(token,nickname,email,firstname,lastname,avatar))


        if (method == "user_alter_password"):
            password    = str(object['password'])
            newpassword = str(object['new_password'])
            self.write(api.user_alter_password(token,password,newpassword))

        if (method == "user_delete"):
            print()



class ShopHandler(tornado.web.RequestHandler):
    def get(self):
        token = self.get_argument('token', True)
    def post(self):
        json_sting = self.request.body
        data_json = tornado.escape.json_decode(json_sting)
        method = str(data_json['type'])
        token = str(data_json['token'])
        secret = str(data_json['secret'])
        object = data_json['object']
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
        token = str(data_json['token'])
        secret = str(data_json['secret'])
        object = data_json['object']
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
        token = str(data_json['token'])
        secret = str(data_json['secret'])
        object = data_json['object']

        if (method == "cost_add"):
            print()


class BasketHandler(tornado.web.RequestHandler):
    def get(self):
        token = self.get_argument('token', True)
    def post(self):
        json_sting = self.request.body
        data_json = tornado.escape.json_decode(json_sting)
        method = str(data_json['type'])
        token = str(data_json['token'])
        secret = str(data_json['secret'])
        object = data_json['object']

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