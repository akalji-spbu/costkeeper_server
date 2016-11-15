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
        secret = self.get_argument('secret', True)

    def post(self):
        json_sting = self.request.body
        data_json = tornado.escape.json_decode(json_sting)
        method = str(data_json['type'])
        token = str(data_json['token'])
        secret = str(data_json['secret'])
        object = data_json['object']
        allowed, userID, response = api.user_check_token(token)
        if(allowed == True):
            if (method == "shop_add"):
                name        = str(object['name'])
                city        = str(object['city'])
                street      = str(object['street'])
                building    = str(object['building'])
                status,response = api.shop_add(name,city, street, building)

            if (method == "shop_alter"):
                id          = str(object['id'])
                name        = str(object['name'])
                city        = str(object['city'])
                street      = str(object['street'])
                building    = str(object['building'])
                status, response = api.shop_alter(id, name, city, street, building)

        self.write(response)



class GoodHandler(tornado.web.RequestHandler):
    def get(self):
        token = self.get_argument('token', True)
        method = self.get_argument('method', True)
        if (method == "good_get"):
            secret = self.get_argument('secret', True)
            good_id = self.get_argument('good_id',True)
            self.write()
        if (method == "good_get_cost"):
            secret = self.get_argument('secret', True)
            good_id = self.get_argument('good_id',True)
            shop_id = self.get_argument('shop_id',True)
            self.write()
        if (method == "good_get_costs_in_all_shops"):
            secret = self.get_argument('secret', True)
            good_id = self.get_argument('good_id',True)
            self.write()
        if (method == "good_get_cost_history_in_shop"):
            secret = self.get_argument('secret', True)
            good_id = self.get_argument('good_id',True)
            shop_id = self.get_argument('shop_id',True)
            self.write()
        if (method == "good_find"):
            secret = self.get_argument('secret', True)
            good_name = self.get_argument('good_name',True)
            self.write()

    def post(self):
        json_sting = self.request.body
        data_json = tornado.escape.json_decode(json_sting)
        method = str(data_json['type'])
        token = str(data_json['token'])
        secret = str(data_json['secret'])
        object = data_json['object']
        if (method == "good_add"):
            barcode = str(data_json['barcode'])
            name = str(data_json['name'])
            life = str(data_json['life'])
            description = str(data_json['description'])
            prod_country_id = str(data_json['prod_country_id'])
            type_id = str(data_json['type_id'])
            picture = str(data_json['picture'])
            print()

        if (method == "good_alter"):
            id = str(data_json['id'])
            barcode = str(data_json['barcode'])
            name = str(data_json['name'])
            life = str(data_json['life'])
            description = str(data_json['description'])
            prod_country_id = str(data_json['prod_country_id'])
            type_id = str(data_json['type_id'])
            picture = str(data_json['picture'])
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