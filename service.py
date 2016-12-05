# -*- coding: utf-8 -*-

import api
import sys
import tornado.web
import tornado.httpserver


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
        allowed, userID, response = api.user_check_token(token)
        object = data_json['object']


        if (method == "user_reg"):
            nickname    = str(object['nickname']).encode('utf-8')
            password    = str(object['password'])
            email       = str(object['email'])
            firstname   = str(object['firstname']).encode('utf-8')
            lastname    = str(object['lastname']).encode('utf-8')
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
                self.write("ERROR_USER_DOES_NOT_EXIST")


        if (method == "user_alter"):
            nickname    = str(object['nickname']).encode('utf-8')
            email       = str(object['email'])
            firstname   = str(object['firstname']).encode('utf-8')
            lastname    = str(object['lastname']).encode('utf-8')
            avatar      = str(object['avatar'])
            self.write(api.user_alter(token,nickname,email,firstname,lastname,avatar))


        if (method == "user_alter_password"):
            password    = str(object['password'])
            newpassword = str(object['new_password'])
            self.write(api.user_alter_password(token,password,newpassword))

        if (method == "user_delete"):
            d_user_id = str(object['d_user_id'])
            status, response = api.user_delete(d_user_id, userID)
            self.write(response)


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
        allowed, user_id, response = api.user_check_token(token)
        if(allowed == True):
            if (method == "shop_add"):
                name        = str(object['name']).encode('utf-8')
                city        = str(object['city'])
                street      = str(object['street'])
                building    = str(object['building']).encode('utf-8')
                status,response = api.shop_add(name,city, street, building)

            if (method == "shop_alter"):
                id          = str(object['id'])
                name        = str(object['name']).encode('utf-8')
                city        = str(object['city'])
                street      = str(object['street'])
                building    = str(object['building']).encode('utf-8')
                status, response = api.shop_alter(id, name, city, street, building)

        self.write(response)


class GoodHandler(tornado.web.RequestHandler):

    def get(self):
        token = self.get_argument('token', True)
        method = self.get_argument('method', True)
        allowed,user_id,response = api.user_check_token(token)
        secret = self.get_argument('secret', True)
        if allowed == True :
            if (method == "good_get"):
                good_id = int(self.get_argument('good_id',True))
                status, response = api.good_get(secret, good_id)

            if (method == "good_get_cost"):
                good_id = int(self.get_argument('good_id',True))
                shop_id = int(self.get_argument('shop_id',True))
                status, response = api.good_get_cost(good_id, shop_id)

            if (method == "good_get_costs_in_all_shops"):
                good_id = int(self.get_argument('good_id',True))
                status, response = api.good_get_costs_in_all_shops(good_id)

            if (method == "good_get_cost_history_in_shop"):
                good_id = int(self.get_argument('good_id',True))
                shop_id = int(self.get_argument('shop_id',True))
                status, response = api.good_get_cost_history_in_shop(good_id, shop_id)
        self.write(response)


    def post(self):
        json_sting = self.request.body
        data_json = tornado.escape.json_decode(json_sting)
        method = str(data_json['type'])
        token = str(data_json['token'])
        secret = str(data_json['secret'])
        allowed,user_id,response = api.user_check_token(token)
        if allowed == True :
            object = data_json['object']
            if (method == "good_add"):
                barcode = str(object['barcode'])
                name = str(object['name']).encode('utf-8')
                life = str(object['life'])
                description = str(object['description']).encode('utf-8')
                prod_country_id = str(object['prod_country_id'])
                type_id = str(object['type_id'])
                picture = str(object['picture'])
                status, response = api.good_add(barcode, name, life, description, prod_country_id, type_id, picture)

            if (method == "good_alter"):
                id = str(object['id'])
                name = str(object['name']).encode('utf-8')
                life = str(object['life'])
                description = str(object['description']).encode('utf-8')
                prod_country_id = str(object['prod_country_id'])
                type_id = str(object['type_id'])
                picture = str(object['picture'])
                status, response = api.good_alter(id, name, life, description, prod_country_id, type_id, picture)
        self.write(response)


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
        allowed, user_id, response = api.user_check_token(token)
        if (allowed == True):
            if (method == "cost_add"):
                good_id         = int(object['good_id'])
                shop_id         = int(object['shop_id'])
                currency_id     = int(object['currency_id'])
                value           = float(object['value'])
                status, response = api.cost_add(good_id, shop_id, currency_id, value)
                return response


class BasketHandler(tornado.web.RequestHandler):
    def get(self):
        token = self.get_argument('token', True)
        method = self.get_argument('method', True)
        allowed,user_id,response = api.user_check_token(token)
        secret = self.get_argument('secret', True)
        if allowed == True :
            if(method == "basket_get"):
                basket_id = self.get_argument('basket_id',True)
                status, response = api.basket_get(basket_id)
            if(method == "basket_get_all"):
                status, response = api.basket_get_all(user_id)
        self.write(response)

    def post(self):
        json_sting = self.request.body
        data_json = tornado.escape.json_decode(json_sting)
        method = str(data_json['type'])
        token = str(data_json['token'])
        secret = str(data_json['secret'])
        allowed, user_id, response = api.user_check_token(token)
        if (allowed == True):
            object = data_json['object']

            if (method == "basket_add"):
                basket_name = str(object['name'])
                status,response = api.basket_add(user_id,basket_name)

            if (method == "basket_delete_item"):
                basket_id = str(object['basket_id'])
                good_id = str(object['good_id'])
                status,response = api.basket_delete_item(user_id,basket_id,good_id)

            if (method == "basket_erase"):
                basket_id = str(object['basket_id'])
                status,response = api.basket_erase(user_id,basket_id)

            if (method == "basket_modify"):
                basket_id = str(object['basket_id'])
                new_name = str(object['new_name'])
                status,response = api.basket_modify(basket_id,new_name)

            if (method == "basket_add_item"):
                basket_id = str(object['basket_id'])
                good_id = int(object['good_id'])
                count = str(object['count'])
                status, response = api.basket_add_item(basket_id, good_id, count)

            if (method == "basket_alter_item"):
                basket_id = str(object['basket_id'])
                good_id = int(object['good_id'])
                count = str(object['count'])
                status, response = api.basket_alter_item(basket_id, good_id, count)

            if (method == "basket_delete"):
                basket_id = str(object['basket_id'])
                status,response = api.basket_delete(user_id, basket_id)

        self.write(response)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [('/user',   UserHandler),
                    ('/shop',   ShopHandler),
                    ('/good',   GoodHandler),
                    ('/cost',   CostHandler),
                    ('/basket', BasketHandler)]
        tornado.web.Application.__init__(self, handlers)



port = 14001
if(len(sys.argv)>0):
    port = sys.argv[1]


# Run the instance
application = Application()
http_server = tornado.httpserver.HTTPServer(application, xheaders=True)
http_server.listen(port)
tornado.ioloop.IOLoop.current().start()