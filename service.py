# -*- coding: utf-8 -*-

import api
import sys
import tornado.web
import tornado.httpserver
import json
import config


class UserHandler(tornado.web.RequestHandler):
    def get(self):
        method = self.get_argument('method', True)
        token = self.get_argument('token', True)
        secret = self.get_argument('secret', True)
        allowed, user_id, response = api.user_check_token(token)
        if allowed:
            if (method == "user_get"):
                ID = self.get_argument('user_id', True)
                status, response = api.user_get(ID)

        self.write(json.dumps(response, ensure_ascii=False).encode('utf8'))

    def post(self):
        json_sting = self.request.body
        data_json = tornado.escape.json_decode(json_sting)
        method = str(data_json['type'])
        token = str(data_json['token'])
        secret = str(data_json['secret'])
        object = data_json['object']
        allowed, user_id, response = api.user_check_token(token)

        if (method == "user_reg"):
            nickname = str(object['nickname']).encode('utf-8')
            password = str(object['password'])
            email = str(object['email'])
            firstname = str(object['firstname']).encode('utf-8')
            lastname = str(object['lastname']).encode('utf-8')
            status, response = api.user_reg(nickname, password, email, firstname, lastname)

        if (method == "user_auth"):
            email = str(object['email'])
            password = str(object['password'])
            status, response = api.user_auth(email, password)

        if allowed:
            if (method == "user_alter"):
                nickname = str(object['nickname']).encode('utf-8')
                email = str(object['email'])
                firstname = str(object['firstname']).encode('utf-8')
                lastname = str(object['lastname']).encode('utf-8')
                avatar = str(object['avatar'])
                status, response = api.user_alter(user_id, nickname, email, firstname, lastname, avatar)

            if (method == "user_alter_password"):
                password = str(object['password'])
                newpassword = str(object['new_password'])
                status, response = api.user_alter_password(token, password, newpassword)

            if (method == "user_delete"):
                d_user_id = str(object['d_user_id'])
                status, response = api.user_delete(user_id, d_user_id)

            if (method == "set_avatar"):
                b64image = str(object['b64image'])
                status, response = api.set_avatar(user_id, b64image)
        self.write(json.dumps(response))


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
        if (allowed == True):
            if (method == "shop_add"):
                name = str(object['name']).encode('utf-8')
                city = str(object['city'])
                street = str(object['street'])
                building = str(object['building']).encode('utf-8')
                status, response = api.shop_add(name, city, street, building)

            if (method == "shop_alter"):
                id = str(object['id'])
                name = str(object['name']).encode('utf-8')
                city = str(object['city'])
                street = str(object['street'])
                building = str(object['building']).encode('utf-8')
                status, response = api.shop_alter(id, name, city, street, building)

        self.write(json.dumps(response))


class GoodHandler(tornado.web.RequestHandler):
    def get(self):
        token = self.get_argument('token', True)
        method = self.get_argument('method', True)
        allowed, user_id, response = api.user_check_token(token)
        secret = self.get_argument('secret', True)
        if allowed == True:
            if (method == "good_get"):
                good_id = int(self.get_argument('good_id', True))
                status, response = api.good_get(good_id)

            if (method == "good_find"):
                find_type = str(self.get_argument('type', True))
                status = False
                response = {"STATUS": "ERROR_WRONG_SEARCH_TYPE"}
                if (find_type == "barcode"):
                    barcode = str(self.get_argument('barcode', True))
                    status, response = api.good_find_by_barcode(barcode)

            if (method == "good_get_cost"):
                good_id = int(self.get_argument('good_id', True))
                shop_id = int(self.get_argument('shop_id', True))
                status, response = api.good_get_cost(good_id, shop_id)

            if (method == "good_get_costs_in_all_shops"):
                good_id = int(self.get_argument('good_id', True))
                status, response = api.good_get_costs_in_all_shops(good_id)

            if (method == "good_get_cost_history_in_shop"):
                good_id = int(self.get_argument('good_id', True))
                shop_id = int(self.get_argument('shop_id', True))
                status, response = api.good_get_cost_history_in_shop(good_id, shop_id)
        self.write(json.dumps(response, ensure_ascii=False).encode('utf8'))

    def post(self):
        json_sting = self.request.body
        data_json = tornado.escape.json_decode(json_sting)
        method = str(data_json['method'])
        token = str(data_json['token'])
        secret = str(data_json['secret'])
        allowed, user_id, response = api.user_check_token(token)
        if allowed == True:
            object = data_json['object']

            if (method == "good_add"):
                barcode = str(object['barcode'])
                name = str(object['name']).encode('utf-8')
                life = str(object['life'])
                description = str(object['description']).encode('utf-8')
                type_id = str(object['type_id'])
                units_id = str(object['units_id'])
                alcohol = str(object['alcohol'])
                manufacturer_id = str(object['manufacturer_id'])
                b64 = str(object['b64'])
                brand = str(object['brand']).encode('utf-8')
                prod_country_id = str(object['prod_country_id'])
                status, response = api.good_add(barcode, name, life, description, type_id, units_id, alcohol,
                                                manufacturer_id, b64, brand, prod_country_id)

            if (method == "good_add_ean13"):
                barcode = str(object['barcode'])
                name = str(object['name']).encode('utf-8')
                barcode_type = str(object['barcode_type']).encode('utf-8')
                description = str(object['description']).encode('utf-8')
                country = str(object['country']).encode('utf-8')
                manufacturer = str(object['manufacturer']).encode('utf-8')
                picture_b64 = str(object['picture_b64'])
                brand = str(object['brand']).encode('utf-8')
                category = str(object['category']).encode('utf-8')
                status, response = api.good_add_ean13(barcode, name, barcode_type, country, manufacturer, picture_b64,
                                                      brand, description, category)

            if (method == "good_add_by_server"):
                barcode = str(object['barcode'])
                status, response = api.good_add_by_server(barcode)

            if (method == "good_alter"):
                id = str(object['id'])
                name = str(object['name']).encode('utf-8')
                life = str(object['life'])
                description = str(object['description']).encode('utf-8')
                type_id = str(object['type_id'])
                units_id = str(object['units_id'])
                alcohol = str(object['alcohol'])
                manufacturer_id = str(object['manufacturer_id'])
                b64 = str(object['b64'])
                brand = str(object['brand']).encode('utf-8')
                prod_country_id = str(object['prod_country_id'])
                status, response = api.good_alter(id, name, life, description, type_id, units_id, alcohol,
                                                  manufacturer_id, b64, brand, prod_country_id)
        self.write(json.dumps(response, ensure_ascii=False).encode('utf8'))


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
                good_id = int(object['good_id'])
                shop_id = int(object['shop_id'])
                currency_id = int(object['currency_id'])
                value = float(object['value'])
                status, response = api.cost_add(good_id, shop_id, currency_id, value)
                self.write(json.dumps(response, ensure_ascii=False).encode('utf8'))


class BasketHandler(tornado.web.RequestHandler):
    def get(self):
        token = self.get_argument('token', True)
        method = self.get_argument('method', True)
        allowed, user_id, response = api.user_check_token(token)
        secret = self.get_argument('secret', True)
        if allowed == True:
            if (method == "basket_get"):
                basket_id = self.get_argument('basket_id', True)
                status, response = api.basket_get(basket_id)
            if (method == "basket_get_all"):
                status, response = api.basket_get_all(user_id)
            if (method == "basket_get_lowest_cost"):
                basket_id = int(self.get_argument('basket_id', True))
                shop_list = list(self.get_argument('shop_list', True))
                status, response = api.basket_get_lowest_cost(shop_list, basket_id)
        self.write(json.dumps(response, ensure_ascii=False).encode('utf8'))

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
                status, response = api.basket_add(user_id, basket_name)

            if (method == "basket_delete_item"):
                basket_id = str(object['basket_id'])
                good_id = str(object['good_id'])
                status, response = api.basket_delete_item(user_id, basket_id, good_id)

            if (method == "basket_erase"):
                basket_id = str(object['basket_id'])
                status, response = api.basket_erase(user_id, basket_id)

            if (method == "basket_modify"):
                basket_id = str(object['basket_id'])
                new_name = str(object['new_name'])
                status, response = api.basket_modify(basket_id, new_name)

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
                status, response = api.basket_delete(user_id, basket_id)

        self.write(json.dumps(response, ensure_ascii=False).encode('utf8'))


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [('/user', UserHandler),
                    ('/shop', ShopHandler),
                    ('/good', GoodHandler),
                    ('/cost', CostHandler),
                    ('/basket', BasketHandler)]
        tornado.web.Application.__init__(self, handlers)


try:
    port = sys.argv[1]
except:
    port = config.port

# Run the instance
application = Application()
http_server = tornado.httpserver.HTTPServer(application, xheaders=True)
http_server.listen(port)
print("Starting service on port " + str(port))
tornado.ioloop.IOLoop.current().start()
