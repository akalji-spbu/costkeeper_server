# -*- coding: utf-8 -*-

import config
import costkeeper
import sqlalchemy.exc
import random
import string
import datetime
from datetime import datetime, timedelta
from hashlib import md5
from sqlalchemy import create_engine, select, delete, and_, or_
from sqlalchemy.sql import table, column
from sqlalchemy.orm import sessionmaker
from sqlalchemy import TEXT, INTEGER, String

dburi = config.db_dialect + '://' + config.db_user + ':' + config.db_password + '@' + config.db_host + ':' +config.db_port+ '/'+ config.db_name +'?charset=utf8'

#users methods

def user_is_admin(user_id):
    return False

def user_check_token(token):
    # Creating database session
    engine = create_engine(dburi)
    conn = engine.connect()
    # /Creating database session
    allowed = False
    userID = ""

    select_stmt = select([costkeeper.User.token_lifetime, costkeeper.User.User_ID]).where(costkeeper.User.token == token)
    result = conn.execute(select_stmt)
    rows = result.fetchall()
    result.close()

    if not rows:
        response = "ERROR_TOKEN_DOES_NOT_EXIST"
    else:
        if (rows[0].token_lifetime < datetime.today()):
            response = "ERROR_TOKEN_EXSPIRED"
        else:
            allowed = True
            userID = rows[0].User_ID
            response = "TOKEN_ALLOWED"

    return allowed, userID, response

def check_username_and_email(username, email):
    engine = create_engine(dburi)
    conn = engine.connect()
    select_stmt = select([costkeeper.User.User_ID]).where(costkeeper.User.User_Nickname == username)
    result = conn.execute(select_stmt)
    rows = result.fetchall()
    result.close()
    if not rows:
        username_exist = False
    else:
        username_exist = True

    select_stmt = select([costkeeper.User.User_ID]).where(costkeeper.User.User_Email == email)
    result = conn.execute(select_stmt)
    rows = result.fetchall()
    result.close()
    if not rows:
        email_exist = False
    else:
        email_exist = True

    return username_exist, email_exist

def user_auth(email,password):
    # Creating database session
    engine = create_engine(dburi)
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    # /Creating database session
    key = config.salt + ":" + password
    passkey = md5(key.encode('utf-8')).hexdigest()

    select_stmt = select([costkeeper.User.User_ID]).where(costkeeper.User.User_Email == email and costkeeper.User.password==passkey)
    result = conn.execute(select_stmt)
    rows = result.fetchall()
    result.close()

    if not rows:
        status = False
        token = ""
    else:
        User_ID = rows[0].User_ID
        status = True
        a = string.ascii_lowercase + string.digits
        token = ''.join([random.choice(a) for i in range(20)])
        ourUser = session.query(costkeeper.User).filter_by(User_ID=User_ID).first()
        ourUser.token = token
        ourUser.token_lifetime = datetime.today()+timedelta(days=1)
        session.commit()
    return status, token

def user_reg(nickname="", password="", email="", firstname="", lastname="", avatar=""):
    # Creating database session
    engine = create_engine(dburi)
    Session = sessionmaker(bind=engine)
    session = Session()
    # /Creating database session

    key = config.salt + ":" + password
    passkey = md5(key.encode('utf-8')).hexdigest()
    token = ""

    User_Nickname   = nickname
    User_Email      = email
    User_Firstname  = firstname
    User_Lastname   = lastname
    Role_ID         = 1
    avatar          = avatar
    password        = passkey
    token           = ""
    token_lifetime  = 0
    Creation_Date   = datetime.today()


    NewUser = costkeeper.User(User_Nickname, User_Email, User_Firstname, User_Lastname, Role_ID, avatar, password, token, token_lifetime, Creation_Date)
    try:
        session.add(NewUser)
    except sqlalchemy.exc.OperationalError:
        print("ERROR_CORE_ADDING")

    session.commit()
    return True

def user_alter(token="",nickname="",email="",firstname="",lastname="",avatar=""):
    # Creating database session
    engine = create_engine(dburi)
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    # /Creating database session
    if(len(token) == 0):
        return "ERROR_TOKEN_DOES_NOT_EXIST"
    else:
        select_stmt = select([costkeeper.User.token_lifetime]).where(costkeeper.User.token == token)
        result = conn.execute(select_stmt)
        rows = result.fetchall()
        result.close()
        if not rows:
            return "ERROR_TOKEN_DOES_NOT_EXIST"
        if(rows[0].token_lifetime < datetime.today()):
            return "ERROR_TOKEN_EXSPIRED"
        else:
            ourUser = session.query(costkeeper.User).filter_by(token=token).first()
            if (len(nickname) != 0):
                ourUser.User_Nickname = nickname
            if (len(email) != 0):
                ourUser.User_Email = email
            if (len(firstname) != 0):
                ourUser.User_Firstname = firstname
            if (len(lastname) != 0):
                ourUser.User_Lastname = lastname
            if (len(avatar) != 0):
                ourUser.avatar = avatar
            session.commit()
    session.close()
    return "SUCCESS"

def user_delete(d_user_id, user_id):
    d_user_id = int(d_user_id)
    user_id = int(user_id)
    status = False
    response = ""
    print(d_user_id==user_id)
    if (d_user_id==user_id or user_is_admin(user_id)):
        # Creating database session
        engine = create_engine(dburi)
        Session = sessionmaker(bind=engine)
        conn = engine.connect()
        session = Session()
        # /Creating database session
        select_stmt = select([costkeeper.Basket.Basket_ID]).where(costkeeper.Basket.User_ID == user_id)
        result = conn.execute(select_stmt)
        rows = result.fetchall()
        rowcount = result.rowcount
        result.close()
        for row in rows:
            basket_delete(d_user_id, row.Basket_ID)

        ourUser = session.query(costkeeper.User).filter_by(User_ID=d_user_id).first()
        session.delete(ourUser)
        session.commit()
        session.close()
        status = True
        response = "SUCCEESS"

    return status, response

def user_alter_password(token="",password="",newpassword=""):
    # Creating database session
    engine = create_engine(dburi)
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    # /Creating database session
    if(len(token) == 0):
        return "ERROR_TOKEN_DOES_NOT_EXIST"
    else:
        key = config.salt + ":" + password
        passkey = md5(key.encode('utf-8')).hexdigest()
        select_stmt = select([costkeeper.User.token_lifetime,costkeeper.User.password]).where(costkeeper.User.token == token)
        result = conn.execute(select_stmt)
        rows = result.fetchall()
        result.close()
        if not rows:
            return "ERROR_TOKEN_DOES_NOT_EXIST"
        if(rows[0].token_lifetime < datetime.today()):
            return "ERROR_TOKEN_EXSPIRED"
        if(rows[0].password !=passkey):
            return "ERROR_WRONG_PASSWORD"
        key = config.salt + ":" + newpassword
        passkey = md5(key.encode('utf-8')).hexdigest()
        ourUser = session.query(costkeeper.User).filter_by(token=token).first()
        ourUser.password = passkey
        a = string.ascii_lowercase + string.digits
        token = ''.join([random.choice(a) for i in range(20)])
        ourUser.token = token
        ourUser.token_lifetime = datetime.today()+timedelta(days=1)
        session.commit()
        session.close()
        return token

def user_get(token="",ID="",secret=""):
    # Creating database session
    engine = create_engine(dburi)
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    # /Creating database session
    if (len(token) == 0):
        return "ERROR_TOKEN_DOES_NOT_EXIST"
    else:
        select_stmt = select([costkeeper.User.token_lifetime]).where(costkeeper.User.token == token)
        result = conn.execute(select_stmt)
        rows = result.fetchall()
        result.close()
        if not rows:
            return "ERROR_TOKEN_DOES_NOT_EXIST"
        if (rows[0].token_lifetime < datetime.today()):
            return "ERROR_TOKEN_EXSPIRED"
        select_stmt = select([costkeeper.User.User_ID,costkeeper.User.User_Nickname,costkeeper.User.User_Firstname,costkeeper.User.User_Lastname,costkeeper.User.avatar ]).where(costkeeper.User.User_ID == ID)
        result = conn.execute(select_stmt)
        rows = result.fetchall()
        result.close()
        if not rows:
            session.close()
            return "ERROR_USER_DOES_NOT_EXIST"
        json_data = '{"user_id":"'+str(rows[0].User_ID) +'","nickname": "'+rows[0].User_Nickname +'","firstname":"'+ rows[0].User_Firstname+'","lastname":"'+rows[0].User_Lastname +'","avatar": "'+rows[0].avatar +'"}'
        session.close()
        return json_data

#end users methods


#shops methods
def check_shop_by_id(id):
    engine = create_engine(dburi)
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    select_stmt = select([costkeeper.Shop.Shop_ID]).where(costkeeper.Shop.Shop_ID == id)
    result = conn.execute(select_stmt)
    rows = result.fetchall()
    result.close()
    rows = result.fetchall()
    result.close()
    if not rows:
        return False
    else:
        return True

def check_shop_exist(name, city, street, building):
    engine = create_engine(dburi)
    conn = engine.connect()
    select_stmt = select([costkeeper.Shop.Shop_ID]).where(costkeeper.Shop.Shop_Name == name).where(costkeeper.Shop.City_ID == city).where(costkeeper.Shop.Street_ID == street).where(costkeeper.Shop.Building == building)
    result = conn.execute(select_stmt)
    rows = result.fetchall()
    result.close()
    if not rows:
        return False
    else:
        return True

def shop_add(name="",city="", street="", building=""):
    if(check_shop_exist(name, city, street, building) == False):
        # Creating database session
        engine = create_engine(dburi)
        Session = sessionmaker(bind=engine)
        session = Session()
        # /Creating database session
        Shop_Name   = name
        City_ID     = city
        Street_ID   = street
        Building    = building
        NewShop     = costkeeper.Shop(Shop_Name, City_ID, Street_ID, Building)
        try:
            session.add(NewShop)
            response = "SUCCESS"
            status   = True
            session.commit()
        except sqlalchemy.exc.OperationalError:
            response = "ADDING_ERROR"
            status   = False

    else:
        status = False
        response = "ERROR_SHOP_ALREDY_EXIST"

    return status, response

def shop_alter(id, name,city, street, building):
    # Creating database session
    engine = create_engine(dburi)
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    # /Creating database session
    select_stmt = select([costkeeper.Shop.Shop_ID]).where(costkeeper.User.token == id)
    result = conn.execute(select_stmt)
    rows = result.fetchall()
    result.close()
    if not rows:
        return "ERROR_SHOP_DOES_NOT_EXIST"
    else:
        ourShop = session.query(costkeeper.Shop.Shop_ID).filter_by(Shop_ID=id).first()
        if (len(name) != 0):
            ourShop.Shop_Name = name
        if (len(city) != 0):
            ourShop.City_ID = city
        if (len(street) != 0):
            ourShop.Street_ID = street
        if (len(building) != 0):
            ourShop.Building = building
        session.commit()
        session.close()
        return "SUCCESS"

def shop_get(id):
    # Creating database session
    engine = create_engine(dburi)
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    # /Creating database session
    select_stmt = select([costkeeper.Shop.Shop_ID, costkeeper.Shop.Shop_Name, costkeeper.Shop.City_ID,
                          costkeeper.Shop.Street_ID, costkeeper.Shop.Building]).where(costkeeper.Shop.User_ID == id)

    result = conn.execute(select_stmt)
    rows = result.fetchall()
    result.close()
    if not rows:
        return "ERROR_SHOP_DOES_NOT_EXIST"
    else:
        json_data = '{"shop_id":"'+str(rows[0].Shop_ID) +'","name": "'+rows[0].Shop_Name +'","city_id":"'+ rows[0].City_ID+'","street_id":"'+rows[0].Street_ID +'","building": "'+rows[0].Building +'"}'
        return json_data

#end shops methods

#good methods

def good_add(barcode=0, name="", life="", description="", prod_country_id="", type_id="", picture=""):
    # Creating database session
    engine = create_engine(dburi)
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    # /Creating database session
    status = True
    response = "SUCCESS"

    select_stmt = select([costkeeper.Good.Good_ID]).where(costkeeper.Good.Barcode == barcode)
    result = conn.execute(select_stmt)
    rows = result.fetchall()
    result.close()

    if not rows:
        newGood = costkeeper.Good(name, barcode, life, description, prod_country_id, type_id, picture)
        try:
            session.add(newGood)
        except sqlalchemy.exc.OperationalError:
            status = False
            response = "ADDING_ERROR"
    else:
        status = False
        response = "ERROR_GOOD_ALREADY_EXIST"

    session.commit()
    session.close()
    return status, response

def good_alter(id="", name="", life="", description="", prod_country_id="", type_id="", picture=""):
    # Creating database session
    engine = create_engine(dburi)
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    # /Creating database session

    status = True
    response = "SUCCESS"

    select_stmt = select([costkeeper.Good.Good_ID]).where(costkeeper.Good.Good_ID == id)
    result = conn.execute(select_stmt)
    rows = result.fetchall()
    result.close()

    if not rows:
        status = False
        response = "ERROR_GOOD_DOES_NOT_EXIST"
    else:
        ourGood = session.query(costkeeper.Good).filter_by(Good_ID=id).first()
        if (len(name) != 0):
            ourGood.Name = name
        if (len(life) != 0):
            ourGood.Life = life
        if (len(description) != 0):
            ourGood.Description = description
        if (len(prod_country_id) != 0):
            ourGood.Prod_country_ID = prod_country_id
        if (len(type_id) != 0):
            ourGood.Type = type_id
        if (len(picture) != 0):
            ourGood.Picture = picture

    session.commit()
    session.close()
    return status, response

def good_get(secret="", good_id=""):
    # Creating database session
    engine = create_engine(dburi, encoding='utf-8')
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    # /Creating database session

    status = True

    select_stmt = select([costkeeper.Good.Good_ID]).where(costkeeper.Good.Good_ID == good_id)
    result = conn.execute(select_stmt)
    rows = result.fetchall()
    result.close()

    if not rows:
        status = False
        response = "ERROR_GOOD_DOES_NOT_EXIST"
    else:
        select_stmt = select([costkeeper.Good.Good_ID, costkeeper.Good.Barcode, costkeeper.Good.Life, costkeeper.Good.Description, costkeeper.Good.Name, costkeeper.Good.Picture, costkeeper.Good.Prod_country_ID, costkeeper.Good.Type_ID ]).where(costkeeper.Good.Good_ID == good_id)
        result = conn.execute(select_stmt)
        rows = result.fetchall()
        result.close()
        encoded = rows[0].Description
        print(encoded)
        response = '{"good_id":"'+str(rows[0].Good_ID) +'","barcode": "'+rows[0].Barcode +'","life": "'+rows[0].Life +'","description": "'+rows[0].Description \
                   +'","name": "'+rows[0].Name +'","picture": "'+rows[0].Picture +'","prod_country_id": "'+str(rows[0].Prod_country_ID) +'","type_id": "'+str(rows[0].Type_ID)+'"}'

    return status, response

def good_get_cost(good_id=0, shop_id=0):
    # Creating database session
    engine = create_engine(dburi)
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    # /Creating database session

    status = True
    response = "SUCCESS"

    select_stmt = select([costkeeper.Good.Good_ID]).where(costkeeper.Good.Good_ID == good_id)
    result = conn.execute(select_stmt)
    rows = result.fetchall()
    result.close()
    if not rows or good_id==0:
        status = False
        response = "ERROR_GOOD_DOES_NOT_EXIST"
    else:
        select_stmt = select([costkeeper.Shop.Shop_ID]).where(costkeeper.Shop.Shop_ID == shop_id)
        result = conn.execute(select_stmt)
        rows = result.fetchall()
        result.close()
        if not rows or shop_id == 0:
            status = False
            response = "ERROR_SHOP_DOES_NOT_EXIST"
        else:
            select_stmt = select([costkeeper.Cost.Cost_value,costkeeper.Cost.Currency_ID]).where(costkeeper.Cost.Shop_ID == shop_id).where(costkeeper.Cost.Good_ID == good_id).order_by(costkeeper.Cost.Cost_Time.desc())
            result = conn.execute(select_stmt)
            rows = result.fetchall()
            result.close()
            if not rows:
                status = False
                response = "ERROR_COST_DOES_NOT_EXIST"
            else:
                response = "{\"shop_id\":\" "+str(shop_id)+"\",\"cost\": \""+str(rows[0].Cost_value)+"\",\"currency\":\""+str(rows[0].Currency_ID)+"\"}"
    session.close()
    return status, response

def good_get_costs_in_all_shops(good_id=0):
    # Creating database session
    engine = create_engine(dburi)
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    # /Creating database session

    status = True
    response = "SUCCESS"

    select_stmt = select([costkeeper.Good.Good_ID]).where(costkeeper.Good.Good_ID == good_id)
    result = conn.execute(select_stmt)
    rows = result.fetchall()
    result.close()
    if not rows or good_id==0:
        status = False
        response = "ERROR_GOOD_DOES_NOT_EXIST"
    else:
        select_stmt = select([costkeeper.Cost.Shop_ID]).where(costkeeper.Cost.Good_ID == good_id).distinct(costkeeper.Cost.Shop_ID)
        result = conn.execute(select_stmt)
        rows = result.fetchall()
        i = result.rowcount
        result.close()
        count = 0
        if not rows:
            status = False
            response = "ERROR_COST_DOES_NOT_EXIST"
        else:
            response = "{\"good_id\":\""+str(good_id)+"\",\"costs\":["
            for row in rows:
                count = count +1
                status,r = good_get_cost(good_id,row.Shop_ID)
                response = response + r
                if(count != i):
                    response = response +","
            response = response +"]}"

    return status, response

def good_get_cost_history_in_shop(good_id="", shop_id=""):
    # Creating database session
    engine = create_engine(dburi)
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    # /Creating database session
    status = True
    select_stmt = select([costkeeper.Cost.Cost_Time, costkeeper.Cost.Cost_value, costkeeper.Cost.Currency_ID]).where(costkeeper.Cost.Good_ID == good_id).where(costkeeper.Cost.Shop_ID == shop_id)
    result = conn.execute(select_stmt)
    rows = result.fetchall()
    rowcount = result.rowcount
    result.close()
    if not rows:
        status = False
        response = "ERROR_NO_GOODS_IN_THIS_SHOP"
    else:
        response = '''{"good_id":"''' + str(good_id) + '''","shop_id":"''' + str(good_id) + '''","costs":['''
        cnt = 0
        for row in rows:
            cnt = cnt + 1
            response = response + '''{"datetime":"''' + str(row.Cost_Time) + '''","cost":"''' + str(row.Cost_value) + '''","currency":"''' + str(row.Currency_ID)+ '''"}'''
            if (cnt < rowcount):
                response = response + ","

        response = response + "]}"

    return status, response

def good_find(secret="", good_id=""):
    # Creating database session
    engine = create_engine(dburi)
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    # /Creating database session
    status = True
    response = "SUCCESS"
    return status, response

#end good methods

#Cost methods
def cost_add(good_id='', shop_id='', currency_id='', value=''):
    # Creating database session
    engine = create_engine(dburi)
    Session = sessionmaker(bind=engine)
    session = Session()
    # /Creating database session
    NewCost = costkeeper.Cost(datetime.today(), int(good_id), int(shop_id), int(currency_id), float(value))
    try:
        session.add(NewCost)
        status = True
        response = "SUCSESS"
        session.commit()
        session.close()
    except sqlalchemy.exc.OperationalError:
        response = "COST_ADDING_ERROR"
        status = False
        session.close()

    return status, response

#End cost methods


#basket methods
def basket_add(user_id,basket_name=""):
    # Creating database session
    engine = create_engine(dburi)
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    # /Creating database session

    status = True
    response = "SUCCESS"

    if(len(basket_name) == 0):
        basket_name = "Untitled"
    newBasket = costkeeper.Basket(user_id,datetime.today(),datetime.today(),basket_name)
    try:
        session.add(newBasket)
    except sqlalchemy.exc.OperationalError:
        status = False
        response = "ADDING_ERROR"
    session.commit()
    session.close()
    return status, response


def basket_delete_item(user_id="",basket_id="",good_id=""):
    # Creating database session
    engine = create_engine(dburi)
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    # /Creating database session

    status = True
    response = "SUCCESS"
    select_stmt = select([costkeeper.Basket.User_ID]).where(costkeeper.Basket.Basket_ID == basket_id)
    result = conn.execute(select_stmt)
    rows = result.fetchall()
    result.close()
    if not rows:
        status = False
        response = "ERROR_WRONG_BASKET_ID"
    else:
        if rows[0].User_ID != user_id:
            status = False
            response = "ERROR_ACCESS"
            return status,response

    if(len(basket_id) == 0 and status == True):
        status = False
        response = "ERROR_NO_BASKET_ID"
    else:
        if(len(good_id) == 0):
            status = False
            response = "ERROR_NO_GOOD_ID"
        else:
            ourGoodInBasket = session.query(costkeeper.Good_in_basket).filter_by(Good_ID=good_id).filter_by(Basket_ID=basket_id).first()
            if(ourGoodInBasket == None):
                status = False
                response = "ERROR_GOOD_IN_BASKET_DOES_NOT_EXIST"
            else:
                session.delete(ourGoodInBasket)
    session.commit()
    session.close()
    return status, response


def basket_modify(basket_id,new_name):
    # Creating database session
    engine = create_engine(dburi)
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    # /Creating database session

    status = True
    response = "SUCCESS"

    select_stmt = select([costkeeper.Basket.Basket_ID]).where(costkeeper.Basket.Basket_ID == basket_id)
    result = conn.execute(select_stmt)
    rows = result.fetchall()
    result.close()

    if not rows:
        status = False
        response = "ERROR_BASKET_DOES_NOT_EXIST"
    else:
        ourBasket = session.query(costkeeper.Basket).filter_by(Basket_ID=basket_id).first()
        if(len(new_name) == 0):
            ourBasket.Name = "Untitled"
        else:
            ourBasket.Name = new_name
        ourBasket.Modify_date = datetime.today()
    session.commit()
    session.close()
    return status, response


def basket_erase(user_id,basket_id=""):
    # Creating database session
    engine = create_engine(dburi)
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    # /Creating database session

    status = True
    response = "SUCCESS"

    select_stmt = select([costkeeper.Basket.User_ID]).where(costkeeper.Basket.Basket_ID == basket_id)
    result = conn.execute(select_stmt)
    rows = result.fetchall()
    result.close()
    if not rows:
        status = False
        response = "ERROR_WRONG_BASKET_ID"
        return status, response
    else:
        if rows[0].User_ID != user_id:
            status = False
            response = "ERROR_ACCESS"
            return status, response

    ourGoods = session.query(costkeeper.Good_in_basket).filter_by(Basket_ID=basket_id).all()
    for result in ourGoods:
        session.delete(result)
    session.commit()
    session.close()
    return status, response


def basket_get(basket_id=""):
    # Creating database session
    engine = create_engine(dburi)
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    # /Creating database session

    status = True
    response = "SUCCESS"

    select_stmt = select([costkeeper.Basket.Basket_ID]).where(costkeeper.Basket.Basket_ID == basket_id)
    result = conn.execute(select_stmt)
    rows = result.fetchall()
    result.close()

    if not rows:
        status = False
        response = "BASKET_DOES_NOT_EXIST"
    else:
        select_stmt = select([costkeeper.Basket.Basket_ID,costkeeper.Basket.Name,costkeeper.Basket.Creation_date, costkeeper.Basket.Modify_date ]).where(costkeeper.Basket.Basket_ID == basket_id)
        result = conn.execute(select_stmt)
        rows = result.fetchall()
        result.close()
        response = '{"basket_id":"'+str(rows[0].Basket_ID) +'","name": "'+str(rows[0].Name)+'","creation_date": "'+str(rows[0].Creation_date)+'","modfy_date": "'+str(rows[0].Modify_date)

        select_stmt = select([costkeeper.Good_in_basket.Good_ID, costkeeper.Good_in_basket.Number_of_goods]).where(costkeeper.Good_in_basket.Basket_ID == basket_id)
        result = conn.execute(select_stmt)
        rows = result.fetchall()
        rowcount = result.rowcount
        result.close()
        if not rows:
            response = response +'"}'
        else:
            response = response + "\",\"goods\": ["
            cnt = 0
            for row in rows:
                cnt = cnt+1
                response = response + "{\"good_id\":\"" + str(row.Good_ID) + "\",\"number_of_goods\":\"" + str(row.Number_of_goods)+"\"}"
                if (cnt < rowcount):
                    response = response + ","
            response = response + "]}"

    return status, response


def basket_add_item(basket_id, good_id, count):
    # Creating database session
    engine = create_engine(dburi)
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    # /Creating database session
    select_stmt = select([costkeeper.Basket.Basket_ID]).where(costkeeper.Basket.Basket_ID == basket_id)
    result = conn.execute(select_stmt)
    basketexist = result.fetchall()
    result.close()
    if not basketexist:
        status = False
        response = "ERROR_BASKET_DOES_NOT_EXIST"
    else:
        select_stmt = select([costkeeper.Good_in_basket.Basket_ID, costkeeper.Good_in_basket.Good_ID]).where(costkeeper.Good_in_basket.Basket_ID == basket_id).where(costkeeper.Good_in_basket.Good_ID == good_id)
        result = conn.execute(select_stmt)
        rows = result.fetchall()
        result.close()
        if not rows:
            NewGood_in_basket = costkeeper.Good_in_basket(basket_id, good_id, count)
            try:
                session.add(NewGood_in_basket)
                status = True
                response = "SUCCESS"
            except sqlalchemy.exc.OperationalError:
                response = "ERROR_ADDING"
                status = False
        else:
            ourGood_in_basket = session.query(costkeeper.Good_in_basket).filter(costkeeper.Good_in_basket.Basket_ID == basket_id).filter(costkeeper.Good_in_basket.Good_ID == good_id).first()
            #print(dir(ourGood_in_basket))
            ourGood_in_basket.Number_of_goods = ourGood_in_basket.Number_of_goods + int(count)
            status = True
            response = "SUCCESS"
        if(status==True):
            ourBasket = session.query(costkeeper.Basket).filter_by(Basket_ID=basket_id).first()
            ourBasket.Modify_date = datetime.today()
    session.commit()
    session.close()
    return status, response


def basket_alter_item(basket_id, good_id, count):
    # Creating database session
    engine = create_engine(dburi)
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    # /Creating database session
    select_stmt = select([costkeeper.Basket.Basket_ID]).where(costkeeper.Basket.Basket_ID == basket_id)
    result = conn.execute(select_stmt)
    basketexist = result.fetchall()
    result.close()
    if not basketexist:
        status = False
        response = "ERROR_BASKET_DOES_NOT_EXIST"
    else:
        select_stmt = select([costkeeper.Good_in_basket.Basket_ID, costkeeper.Good_in_basket.Good_ID]).where(costkeeper.Good_in_basket.Basket_ID == basket_id).where(costkeeper.Good_in_basket.Basket_ID == basket_id)
        result = conn.execute(select_stmt)
        rows = result.fetchall()
        result.close()
        if not rows:
            response = "ERROR_GOOD_IN_THE_BASKET_DOES_NOT_EXIST"
            status   = False
        else:
            ourGood_in_basket = session.query(costkeeper.Good_in_basket).filter(costkeeper.Good_in_basket.Basket_ID == basket_id).filter(costkeeper.Good_in_basket.Good_ID == good_id).first()
            ourGood_in_basket.Number_of_goods = int(count)
            status = True
            response = "SUCCESS"
        if(status==True):
            ourBasket = session.query(costkeeper.Basket).filter_by(Basket_ID=basket_id).first()
            ourBasket.Modify_date = datetime.today()
    session.commit()
    session.close()
    return status, response


def basket_delete(user_id, basket_id):
    status = True
    response = "SUCCESS"
    # Creating database session
    engine = create_engine(dburi)
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    # /Creating database session
    ourBasket = session.query(costkeeper.Basket).filter_by(Basket_ID=basket_id).first()
    if ourBasket != None:
        if (ourBasket.User_ID==user_id or user_is_admin(user_id)):
            basket_erase(user_id,basket_id)
            session.delete(ourBasket)
            session.commit()
    else:
        response = "ERROR_BASKET_DOES_NOT_EXISTS"
    session.close()
    session.close()
    return status, response

def basket_get_all(user_id):
    # Creating database session
    engine = create_engine(dburi)
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    # /Creating database session

    status = True
    response = "SUCCESS"

    select_stmt = select([costkeeper.Basket.Basket_ID]).where(costkeeper.Basket.User_ID == user_id)
    result = conn.execute(select_stmt)
    rows = result.fetchall()
    rowcount = result.rowcount
    result.close()

    if not rows:
        status = False
        response = "ERROR_BASKETS_DOES_NOT_EXISTS"
    else:
        select_stmt = select([costkeeper.Basket.Basket_ID, costkeeper.Basket.Name, costkeeper.Basket.Creation_date, costkeeper.Basket.Modify_date]).where(costkeeper.Basket.User_ID == user_id)
        result = conn.execute(select_stmt)
        rows = result.fetchall()
        result.close()
        response = '''{"userID":"''' + str(user_id) + '''","Array": ['''
        cnt = 0
        for row in rows:
            cnt = cnt+1
            response = response + '''{"basketID":"''' + str(row.Basket_ID) + '''","basketName":"''' + row.Name + '''","creationDate":"''' + str(row.Creation_date) + '''","modifiedDate":"''' + str(row.Modify_date) + '''"}'''
            if(cnt < rowcount):
                response = response + ","

        response = response + "]}"
    return status, response
#end basket methods