# -*- coding: utf-8 -*-

import config
import costkeeper
import picture_saver

import sqlalchemy.exc
import random
import string
import datetime
from datetime import datetime, timedelta
from hashlib import md5
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

dburi = config.db_dialect + '://' + config.db_user + ':' + config.db_password + '@' + config.db_host + ':' + config.db_port + '/' + config.db_name + '?charset=utf8'


# users methods


def user_is_admin(user_id):
    return False


def user_check_token(token):
    # Creating database session
    engine = create_engine(dburi)
    conn = engine.connect()
    # /Creating database session
    allowed = False
    userID = ""

    select_stmt = select([costkeeper.User.Token_Lifetime, costkeeper.User.User_ID]).where(
        costkeeper.User.Token == token)
    result = conn.execute(select_stmt)
    rows = result.fetchall()
    result.close()

    if not rows:
        response = {
            "STATUS": "ERROR_TOKEN_DOES_NOT_EXIST"
        }
    else:
        if (rows[0].Token_Lifetime < datetime.today()):
            response = {
                "STATUS": "ERROR_TOKEN_EXSPIRED"
            }
        else:
            allowed = True
            userID = rows[0].User_ID
            response = {
                "STATUS": "TOKEN_ALLOWED"
            }

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


def user_auth(email, password):
    # Creating database session
    engine = create_engine(dburi)
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    # /Creating database session
    key = config.salt + ":" + password
    passkey = md5(key.encode('utf-8')).hexdigest()

    response = {}

    select_stmt = select([costkeeper.User.User_ID]).where(
        costkeeper.User.User_Email == email and costkeeper.User.Password == passkey)
    result = conn.execute(select_stmt)
    rows = result.fetchall()
    result.close()

    if not rows:
        status = False
        response["STATUS"] = "ERROR_USER_NOT_FOUND"
    else:
        User_ID = rows[0].User_ID
        status = True
        a = string.ascii_lowercase + string.digits
        token = ''.join([random.choice(a) for i in range(20)])
        ourUser = session.query(costkeeper.User).filter_by(User_ID=User_ID).first()
        ourUser.Token = token
        ourUser.Token_Lifetime = datetime.today() + timedelta(days=1)
        session.commit()
        response["STATUS"] = "SUCCESS"
        response["token"] = token

    session.close()
    return status, response


def user_reg(nickname="", password="", email="", firstname="", lastname=""):
    # Creating database session
    engine = create_engine(dburi)
    Session = sessionmaker(bind=engine)
    session = Session()
    # /Creating database session

    key = config.salt + ":" + password
    passkey = md5(key.encode('utf-8')).hexdigest()
    response = {

    }
    status = True;

    username_exist, email_exist = check_username_and_email(nickname,email)
    if (email_exist == False) and (username_exist == False):
        User_Nickname = nickname
        User_Email = email
        User_Firstname = firstname
        User_Lastname = lastname
        Role_ID = 1
        password = passkey

        a = string.ascii_lowercase + string.digits
        token = ''.join([random.choice(a) for i in range(20)])
        token_lifetime = datetime.today() + timedelta(days=1)

        Creation_Date = datetime.today()

        NewUser = costkeeper.User(User_Nickname, User_Email, User_Firstname, User_Lastname, Role_ID, password,
                                  token, token_lifetime, Creation_Date)
        try:
            session.add(NewUser)
        except sqlalchemy.exc.OperationalError:
            pass

        session.commit()
        response["STATUS"] = "SUCCESS"
        response["OBJECT"] = {"token":token}
    else:
        status = False;
        if email_exist == True:
            response["STATUS"] = "ERROR_EMAIL_EXIST"
        else:
            response["STATUS"] = "ERROR_USERNAME_EXIST"


    session.close()

    return status,response


def user_alter(User_ID,nickname="", email="", firstname="", lastname=""):
    # Creating database session
    engine = create_engine(dburi)
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    # /Creating database session

    status = False
    ourUser = session.query(costkeeper.User).filter_by(User_ID=User_ID).first()
    if (len(nickname) != 0):
        ourUser.User_Nickname = nickname
    if (len(email) != 0):
        ourUser.User_Email = email
    if (len(firstname) != 0):
        ourUser.User_Firstname = firstname
    if (len(lastname) != 0):
        ourUser.User_Lastname = lastname
    session.commit()
    response = {
        "STATUS": "SUCCESS"
    }
    status = True
    session.close()

    return status, response


def user_delete(user_id,d_user_id):
    d_user_id = int(d_user_id)
    user_id = int(user_id)
    status = False
    response ={
        "STATUS": "ERROR_YOU_IS_NOT_GOD"
    }
    if (d_user_id == user_id or user_is_admin(user_id)):
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
        response = {
            "STATUS": "SUCCESS"
        }

    return status, response


def user_alter_password(token="", password="", newpassword=""):
    # Creating database session
    engine = create_engine(dburi)
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    # /Creating database session
    status = False
    if (len(token) == 0):
        response = {
            "STATUS": "ERROR_TOKEN_DOES_NOT_EXIST"
        }
    else:
        key = config.salt + ":" + password
        passkey = md5(key.encode('utf-8')).hexdigest()
        select_stmt = select([costkeeper.User.Token_Lifetime, costkeeper.User.Password]).where(
            costkeeper.User.Token == token)
        result = conn.execute(select_stmt)
        rows = result.fetchall()
        result.close()
        if not rows:
            response = {
                "STATUS": "ERROR_TOKEN_DOES_NOT_EXIST"
            }
        elif (rows[0].Token_Lifetime < datetime.today()):
            response = {
                "STATUS": "ERROR_TOKEN_EXSPIRED"
            }
        elif (rows[0].password != passkey):
            response = {
                "STATUS": "ERROR_WRONG_PASSWORD"
            }
        else:
            key = config.salt + ":" + newpassword
            passkey = md5(key.encode('utf-8')).hexdigest()
            ourUser = session.query(costkeeper.User).filter_by(token=token).first()
            ourUser.password = passkey
            a = string.ascii_lowercase + string.digits
            token = ''.join([random.choice(a) for i in range(20)])
            ourUser.token = token
            ourUser.token_lifetime = datetime.today() + timedelta(days=1)
            session.commit()
            session.close()
            response = {
                "STATUS": "SUCCESS",
                "token": token
            }
            status = True
        return status, response


def user_get(ID=""):
    # Creating database session
    engine = create_engine(dburi)
    conn = engine.connect()
    # /Creating database session
    status = False
    select_stmt = select([costkeeper.User.User_ID, costkeeper.User.User_Nickname, costkeeper.User.User_Firstname,
                          costkeeper.User.User_Lastname]).where(
        costkeeper.User.User_ID == ID)
    result = conn.execute(select_stmt)
    rows = result.fetchall()
    result.close()
    if not rows:
        response = {
            "STATUS": "ERROR_USER_DOES_NOT_EXIST"
        }
    else:
        object = {
            "User_Id": str(rows[0].User_ID),
            "Nickname": rows[0].User_Nickname,
            "Firstname": rows[0].User_Firstname,
            "Lastname": rows[0].User_Lastname,
        }
        response = {
            "STATUS": "SUCCESS",
            "OBJECT": object
        }
        status = True
    return status, response


def set_avatar(user_id, b64image):
    status, response = picture_saver.save_b64_picture(b64image, config.users_avatars_folder, str(user_id))
    return status, response


# end users methods


# shops methods

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
    select_stmt = select([costkeeper.Shop.Shop_ID]).where(costkeeper.Shop.Shop_Name == name).where(
        costkeeper.Shop.City_ID == city).where(costkeeper.Shop.Street_ID == street).where(
        costkeeper.Shop.Building == building)
    result = conn.execute(select_stmt)
    rows = result.fetchall()
    result.close()
    if not rows:
        return False
    else:
        return True


def shop_add(name="", city="", street="", building=""):
    if (check_shop_exist(name, city, street, building) == False):
        # Creating database session
        engine = create_engine(dburi)
        Session = sessionmaker(bind=engine)
        session = Session()
        # /Creating database session
        Shop_Name = name
        City_ID = city
        Street_ID = street
        Building = building
        NewShop = costkeeper.Shop(Shop_Name, City_ID, Street_ID, Building)
        try:
            session.add(NewShop)
            response = {
                "STATUS": "SUCCESS"
            }
            status = True
            session.commit()
        except sqlalchemy.exc.OperationalError:
            response = {
                "STATUS": "ERRROR_ADDING"
            }
            status = False

    else:
        status = False
        response = {
            "STATUS": "ERROR_SHOP_ALREDY_EXIST"
        }

    return status, response


def shop_alter(id, name, city, street, building):
    # Creating database session
    engine = create_engine(dburi)
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    # /Creating database session
    select_stmt = select([costkeeper.Shop.Shop_ID]).where(costkeeper.User.Token == id)
    result = conn.execute(select_stmt)
    rows = result.fetchall()
    result.close()
    if not rows:
        response = {
            "STATUS": "ERROR_SHOP_DOES_NOT_EXIST"
        }
        status = False
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
        status = True
        response = {
            "STATUS": "SUCCESS"
        }
    return status, response


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
        response = {
            "STATUS": "ERROR_SHOP_DOES_NOT_EXIST"
        }
        status = False
    else:
        object = {
            "Shop_ID": str(rows[0].Shop_ID),
            "Name": rows[0].Shop_Name,
            "City_ID": rows[0].City_ID,
            "Street_id": rows[0].Street_ID,
            "Building": rows[0].Building

        }
        response = {
            "STATUS": "SUCCESS",
            "OBJECT": object
        }
        status = True
    return status,response


# end shops methods

# good methods

def good_add(barcode=0, name="", life="", description="", type_id="", units_id="", alcohol="", brand="", b64=""):
    # Creating database session
    engine = create_engine(dburi)
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    # /Creating database session
    status = True
    response = {
        "STATUS": "SUCCESS"
    }

    select_stmt = select([costkeeper.Good.Good_ID]).where(costkeeper.Good.Barcode == barcode)
    result = conn.execute(select_stmt)
    rows = result.fetchall()
    result.close()

    if not rows:
        newGood = costkeeper.Good(name, barcode, life, description, type_id, units_id, alcohol, brand)
        try:
            session.add(newGood)

        except sqlalchemy.exc.OperationalError:
            status = False
            response = {
                "STATUS": "ERROR_ADDING"
            }
    else:
        status = False
        response = {
            "STATUS": "ERROR_GOOD_ALREADY_EXIST"
        }

    session.commit()
    if status:
        picture_saver.save_b64_picture(b64, config.goods_pictures_folder, barcode)
    session.close()

    return status, response


def good_barcode_parse_from_another_service (barcode=0):
    # Creating database session
    engine = create_engine(dburi)
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    # /Creating database session

    import ean13parser, picture_saver
    status,dataset = ean13parser.getGoodInfoByBarcode(barcode)
    select_stmt = select([costkeeper.Country.Country_ID]).where(costkeeper.Country.Country_Name == dataset["country"])
    rows = (conn.execute(select_stmt)).fetchall()
    country_id =''
    for row in rows:
        country_id = row

    select_stmt = select([costkeeper.Type_of_good.Type_ID_ID]).where(costkeeper.Type_of_good.Name == dataset["category"])
    rows = (conn.execute(select_stmt)).fetchall()
    type_id =''
    for row in rows:
        type_id = row

    session.close()

    if status:
        status,response = good_add(dataset["barcode"],dataset["name"],dataset["description"],country_id,type_id,dataset["picture_uri"])
    else:
        response = {
            "STATUS": "ERROR_PARSE_HAS_BEEN_FAILED"
        }

    return status,response


def good_alter(id="", name="", life="", description="", type_id="", units_id="", alcohol="", brand="", b64=""):
    # Creating database session
    engine = create_engine(dburi)
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    # /Creating database session

    status = True
    response = {
        "STATUS": "SUCCESS"
    }

    select_stmt = select([costkeeper.Good.Good_ID]).where(costkeeper.Good.Good_ID == id)
    result = conn.execute(select_stmt)
    rows = result.fetchall()
    result.close()

    if not rows:
        status = False
        response = {
            "STATUS": "ERROR_GOOD_DOES_NOT_EXIST"
        }
    else:
        ourGood = session.query(costkeeper.Good).filter_by(Good_ID=id).first()
        if (len(name) != 0):
            ourGood.Name = name
        if (len(life) != 0):
            ourGood.Life = life
        if (len(description) != 0):
            ourGood.Description = description
        if (len(units_id) != 0):
            ourGood.Units_ID = units_id
        if (len(type_id) != 0):
            ourGood.Type = type_id
        if (len(alcohol) != 0):
            ourGood.Alcohol = alcohol
        if (len(brand) != 0):
            ourGood.Brand = brand
        if (len(b64) != 0):
            picture_saver.save_b64_picture(b64, config.goods_pictures_folder, barcode)
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
        response = {
            "STATUS": "ERROR_GOOD_DOES_NOT_EXIST"
        }
    else:
        select_stmt = select(
            [costkeeper.Good.Good_ID, costkeeper.Good.Barcode, costkeeper.Good.Life, costkeeper.Good.Description,
             costkeeper.Good.Name]).where(costkeeper.Good.Good_ID == good_id)
        print("1")
        result = conn.execute(select_stmt)
        print("2")
        rows = result.fetchall()
        print("3")
        result.close()
        encoded = rows[0].Description
        print("4")
        print(encoded)
        object = {"Good_ID": str(rows[0].Good_ID),
                  "Barcode": rows[0].Barcode,
                  "Life": rows[0].Life,
                  "Description": rows[0].Description,
                  "Name": rows[0].Name,
                  "Type_ID": str(rows[0].Type_ID),
                  "Units_ID": str(rows[0].Units_ID),
                  "Alcohol": str(rows[0].Alcohol),
                  "Brand": rows[0].Brand
                  }
        print("Meow")
        response = {
            "STATUS": "SUCCESS",
            "OBJECT": object
        }

    return status, response


def good_get_cost(good_id=0, shop_id=0):
    # Creating database session
    engine = create_engine(dburi)
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    # /Creating database session

    status = True

    select_stmt = select([costkeeper.Good.Good_ID]).where(costkeeper.Good.Good_ID == good_id)
    result = conn.execute(select_stmt)
    rows = result.fetchall()
    result.close()
    if not rows or good_id == 0:
        status = False
        response = {
            "STATUS": "ERROR_GOOD_DOES_NOT_EXIST"
        }
    else:
        select_stmt = select([costkeeper.Shop.Shop_ID]).where(costkeeper.Shop.Shop_ID == shop_id)
        result = conn.execute(select_stmt)
        rows = result.fetchall()
        result.close()
        if not rows or shop_id == 0:
            status = False
            response = {
                "STATUS": "ERROR_SHOP_DOES_NOT_EXIST"
            }
        else:
            select_stmt = select([costkeeper.Cost.Cost_Value, costkeeper.Cost.Currency_ID]).where(
                costkeeper.Cost.Shop_ID == shop_id).where(costkeeper.Cost.Good_ID == good_id).order_by(
                costkeeper.Cost.Cost_Time.desc())
            result = conn.execute(select_stmt)
            rows = result.fetchall()
            result.close()
            if not rows:
                status = False
                response = {
                    "STATUS": "ERROR_COST_DOES_NOT_EXIST"
                }
            else:
                object = {
                    "Shop_ID": str(shop_id),
                    "Cost": str(rows[0].Cost_Value),
                    "Currency": str(rows[0].Currency_ID)
                }
                response = {
                    "STATUS": "SUCCEESS",
                    "OBJECT": object
                }
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

    select_stmt = select([costkeeper.Good.Good_ID]).where(costkeeper.Good.Good_ID == good_id)
    result = conn.execute(select_stmt)
    rows = result.fetchall()
    result.close()
    if not rows or good_id == 0:
        status = False
        response = {
            "STATUS": "ERROR_GOOD_DOES_NOT_EXIST"
        }
    else:
        select_stmt = select([costkeeper.Cost.Shop_ID]).where(costkeeper.Cost.Good_ID == good_id).distinct(
            costkeeper.Cost.Shop_ID)
        result = conn.execute(select_stmt)
        rows = result.fetchall()
        i = result.rowcount
        result.close()
        count = 0
        if not rows:
            status = False
            response = {
                "STATUS": "ERROR_COST_DOES_NOT_EXIST"
            }
        else:
            costs = []
            for row in rows:
                status, r = good_get_cost(good_id, row.Shop_ID)
                costs.append(r["OBJECT"])

            object = {
                "Good_ID:str(good_id)"
                "Costs": costs
            }

            response = {
                "STATUS": "SUCCESS",
                "OBJECT": object
            }

    return status, response


def good_get_cost_history_in_shop(good_id="", shop_id=""):
    # Creating database session
    engine = create_engine(dburi)
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    # /Creating database session
    status = True
    select_stmt = select([costkeeper.Cost.Cost_Time, costkeeper.Cost.Cost_Value, costkeeper.Cost.Currency_ID]).where(
        costkeeper.Cost.Good_ID == good_id).where(costkeeper.Cost.Shop_ID == shop_id)
    result = conn.execute(select_stmt)
    rows = result.fetchall()
    rowcount = result.rowcount
    result.close()
    if not rows:
        status = False
        response = {
            "STATUS": "ERROR_NO_GOODS_IN_THIS_SHOP"
        }
    else:
        costs = []
        for row in rows:
            costs.append(
                {
                    "Datetime": str(row.Cost_Time),
                    "Cost": str(row.Cost_Value),
                    "Currency": str(row.Currency_ID)
                }
            )
        object = {
            "Good_ID": str(good_id),
            "Shop_ID": str(shop_id),
            "Costs": costs
        }

        response = {
            "STATUS": "SUCCESS",
            "OBJECT": object
        }

    return status, response


def good_find(secret="", good_id=""):
    # Creating database session
    engine = create_engine(dburi)
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    # /Creating database session
    status = True
    response = {
        "STATUS": "SUCCESS"
    }
    return status, response


# end good methods

# Cost methods

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
        response = {
            "STATUS":"SUCCESS"
        }
        session.commit()
        session.close()
    except sqlalchemy.exc.OperationalError:
        response = {
            "STATUS":"ERROR_ADDING_COST"
        }
        status = False
        session.close()

    return status, response


# End cost methods


# basket methods
def basket_add(user_id, basket_name=""):
    # Creating database session
    engine = create_engine(dburi)
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    # /Creating database session

    status = True
    response = {
        "STATUS": "SUCCESS"
    }

    if (len(basket_name) == 0):
        basket_name = "Untitled"
    newBasket = costkeeper.Basket(user_id, datetime.today(), datetime.today(), basket_name)
    try:
        session.add(newBasket)
    except sqlalchemy.exc.OperationalError:
        status = False
        response = {
            "STATUS": "ERROR_ADDING"
        }
    session.commit()
    session.close()
    return status, response


def basket_delete_item(user_id="", basket_id="", good_id=""):
    # Creating database session
    engine = create_engine(dburi)
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    # /Creating database session

    status = True
    response = {
        "STATUS": "SUCCESS"
    }
    select_stmt = select([costkeeper.Basket.User_ID]).where(costkeeper.Basket.Basket_ID == basket_id)
    result = conn.execute(select_stmt)
    rows = result.fetchall()
    result.close()
    if not rows:
        status = False
        response = {
            "STATUS": "ERROR_WRONG_BASKET_ID"
        }
    else:
        if rows[0].User_ID != user_id and user_is_admin(user_id) == False:
            status = False
            response = {
                "STATUS": "ERROR_ACCESS"
            }
            return status, response

    if (len(basket_id) == 0 and status == True):
        status = False
        response = {
            "STATUS":"ERROR_NO_BASKET_ID"
        }
    else:
        if (len(good_id) == 0):
            status = False
            response = {
                "STATUS":"ERROR_NO_GOOD_ID"
            }
        else:
            ourGoodInBasket = session.query(costkeeper.Good_in_basket).filter_by(Good_ID=good_id).filter_by(
                Basket_ID=basket_id).first()
            if (ourGoodInBasket == None):
                status = False
                response = {
                    "STATUS":"ERROR_GOOD_IN_BASKET_DOES_NOT_EXIST"
                }
            else:
                session.delete(ourGoodInBasket)
    session.commit()
    session.close()
    return status, response


def basket_modify(basket_id, new_name):
    # Creating database session
    engine = create_engine(dburi)
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    # /Creating database session

    status = True
    response = {
        "STATUS":"SUCCESS"
    }

    select_stmt = select([costkeeper.Basket.Basket_ID]).where(costkeeper.Basket.Basket_ID == basket_id)
    result = conn.execute(select_stmt)
    rows = result.fetchall()
    result.close()

    if not rows:
        status = False
        response = {
            "STATUS":"ERROR_BASKET_DOES_NOT_EXIST"
        }
    else:
        ourBasket = session.query(costkeeper.Basket).filter_by(Basket_ID=basket_id).first()
        if (len(new_name) == 0):
            ourBasket.Name = "Untitled"
        else:
            ourBasket.Name = new_name
        ourBasket.Modify_Date = datetime.today()
    session.commit()
    session.close()
    return status, response


def basket_erase(user_id, basket_id=""):
    # Creating database session
    engine = create_engine(dburi)
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    # /Creating database session

    status = True
    response = {
        "STATUS":"SUCCESS"
    }

    select_stmt = select([costkeeper.Basket.User_ID]).where(costkeeper.Basket.Basket_ID == basket_id)
    result = conn.execute(select_stmt)
    rows = result.fetchall()
    result.close()
    if not rows:
        status = False
        response = {
            "STATUS":"ERROR_WRONG_BASKET_ID"
        }
        return status, response
    else:
        if rows[0].User_ID != user_id and user_is_admin(user_id) == False:
            status = False
            response = {
                "STATUS":"ERROR_ACCESS"
            }
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

    select_stmt = select([costkeeper.Basket.Basket_ID]).where(costkeeper.Basket.Basket_ID == basket_id)
    result = conn.execute(select_stmt)
    rows = result.fetchall()
    result.close()

    if not rows:
        status = False
        response = {
            "STATUS":"ERROR_BASKET_DOES_NOT_EXIST"
        }
    else:
        select_stmt = select([costkeeper.Basket.Basket_ID, costkeeper.Basket.Name, costkeeper.Basket.Creation_Date,
                              costkeeper.Basket.Modify_Date]).where(costkeeper.Basket.Basket_ID == basket_id)
        result = conn.execute(select_stmt)
        rows = result.fetchall()
        result.close()
        select_stmt = select([costkeeper.Good_in_basket.Good_ID, costkeeper.Good_in_basket.Number_Of_Goods]).where(
            costkeeper.Good_in_basket.Basket_ID == basket_id)
        result = conn.execute(select_stmt)
        new_rows = result.fetchall()
        result.close()
        goods = []
        if new_rows:
            for row in new_rows:
                goods.append(
                    {
                        "good_id":str(row.Good_ID),
                        "number_of_goods":str(row.Number_Of_Goods)
                    }
                )

        basket = {
            "basket_id":str(rows[0].Basket_ID),
            "name":str(rows[0].Name),
            "creation_date":str(rows[0].Creation_Date),
            "modify_date":str(rows[0].Modify_Date),
            "goods":goods
        }
        response = {
            "STATUS":"SUCCESS",
            "OBJECT":basket
        }

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
        response = {
            "STATUS": "ERROR_BASKET_DOES_NOT_EXIST"
        }
    else:
        select_stmt = select([costkeeper.Good_in_basket.Basket_ID, costkeeper.Good_in_basket.Good_ID]).where(
            costkeeper.Good_in_basket.Basket_ID == basket_id).where(costkeeper.Good_in_basket.Good_ID == good_id)
        result = conn.execute(select_stmt)
        rows = result.fetchall()
        result.close()
        if not rows:
            NewGood_in_basket = costkeeper.Good_in_basket(basket_id, good_id, count)
            try:
                session.add(NewGood_in_basket)
                status = True
                response = {
                    "STATUS": "SUCCESS"
                }
            except sqlalchemy.exc.OperationalError:
                response = {
                    "STATUS": "ERROR_ADDING"
                }
                status = False
        else:
            ourGood_in_basket = session.query(costkeeper.Good_in_basket).filter(
                costkeeper.Good_in_basket.Basket_ID == basket_id).filter(
                costkeeper.Good_in_basket.Good_ID == good_id).first()
            ourGood_in_basket.Number_Of_Goods = ourGood_in_basket.Number_Of_Goods + int(count)
            status = True
            response = {
                "STATUS": "SUCCESS"
            }
        if (status == True):
            ourBasket = session.query(costkeeper.Basket).filter_by(Basket_ID=basket_id).first()
            ourBasket.Modify_Date = datetime.today()
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
        response = {
            "STATUS": "ERROR_BASKET_DOES_NOT_EXIST"
        }
    else:
        select_stmt = select([costkeeper.Good_in_basket.Basket_ID, costkeeper.Good_in_basket.Good_ID]).where(
            costkeeper.Good_in_basket.Basket_ID == basket_id).where(costkeeper.Good_in_basket.Basket_ID == basket_id)
        result = conn.execute(select_stmt)
        rows = result.fetchall()
        result.close()
        if not rows:
            response = {
                "STATUS": "ERROR_GOOD_IN_THE_BASKET_DOES_NOT_EXIST"
            }
            status = False
        else:
            ourGood_in_basket = session.query(costkeeper.Good_in_basket).filter(
                costkeeper.Good_in_basket.Basket_ID == basket_id).filter(
                costkeeper.Good_in_basket.Good_ID == good_id).first()
            ourGood_in_basket.Number_Of_Goods = int(count)
            status = True
            response = {
                "STATUS": "SUCCESS"
            }
        if (status == True):
            ourBasket = session.query(costkeeper.Basket).filter_by(Basket_ID=basket_id).first()
            ourBasket.Modify_Date = datetime.today()
    session.commit()
    session.close()
    return status, response


def basket_delete(user_id, basket_id):
    status = True
    response = {
        "STATUS": "SUCCESS"
    }
    # Creating database session
    engine = create_engine(dburi)
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    # /Creating database session
    ourBasket = session.query(costkeeper.Basket).filter_by(Basket_ID=basket_id).first()
    if ourBasket != None:
        if (ourBasket.User_ID == user_id or user_is_admin(user_id)):
            basket_erase(user_id, basket_id)
            session.delete(ourBasket)
            session.commit()
    else:
        response = {
            "STATUS": "ERROR_BASKET_DOES_NOT_EXISTS"
        }
        status = False
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

    select_stmt = select([costkeeper.Basket.Basket_ID]).where(costkeeper.Basket.User_ID == user_id)
    result = conn.execute(select_stmt)
    rows = result.fetchall()
    rowcount = result.rowcount
    result.close()

    if not rows:
        status = False
        response = {
            "STATUS": "ERROR_BASKETS_DOES_NOT_EXISTS"
        }
    else:
        select_stmt = select([costkeeper.Basket.Basket_ID, costkeeper.Basket.Name, costkeeper.Basket.Creation_Date,
                              costkeeper.Basket.Modify_Date]).where(costkeeper.Basket.User_ID == user_id)
        result = conn.execute(select_stmt)
        rows = result.fetchall()
        result.close()
        baskets = []
        for row in rows:
            baskets.append(
                {
                    "Basket_ID": str(row.Basket_ID),
                    "Basket_Name": row.Name,
                    "Creation_Date": str(row.Creation_Date),
                    "Modified_Date": str(row.Modify_Date)
                }
            )
        object = {
            "User_ID": str(user_id),
            "Baskets": baskets
        }

        response = {
            "STATUS": "SUCCESS",
            "OBJECT": object
        }
    return status, response


def basket_get_lowest_cost(shops_list, basket_id):
    # Creating database session
    engine = create_engine(dburi)
    conn = engine.connect()
    # /Creating database session

    status = True

    min_sum = -1.
    m_shop = ""

    if not shops_list:
        status = False
        response ={
            "STATUS": "ERROR_SHOPS_LIST_IS_EMPTY"
        }
    else:
        select_stmt = select([costkeeper.Good_in_basket.Good_ID]).where(
            costkeeper.Good_in_basket.Basket_ID == basket_id)
        result = conn.execute(select_stmt)
        rows = result.fetchall()
        rowcount = result.rowcount
        result.close()
        if not rows:
            status = False
            response = {
                "STATUS": "ERROR_BASKET_IS_EMPTY"
            }
        else:
            current_sum = 0
            cur_shop = ""
            for shop in shops_list:
                cur_shop = shop
                costs_of_goods = engine.execute(
                    "SELECT goods_in_baskets.Good_ID, goods_in_baskets.Number_Of_Goods, costs.Cost_Value, costs.Cost_Time FROM goods_in_baskets  LEFT JOIN costs ON goods_in_baskets.Good_ID=costs.Good_ID WHERE costs.Cost_Time IN (SELECT MAX( costs.Cost_Time ) FROM costs WHERE Shop_ID=shop_id GROUP BY costs.Good_ID)")
                if (costs_of_goods.rowcount < rowcount):
                    current_sum = -2
                else:
                    for item in costs_of_goods:
                        current_sum = current_sum + item.Number_Of_Goods * item.Cost_Value
                if min_sum == -1 or min_sum > current_sum:
                    min_sum = current_sum
                    m_shop = cur_shop
            if (min_sum == -1):
                response = {
                    "STATUS": "ERROR_SHOP_WITH_THIS_GOODS_DOES_NOT_EXIST"
                }
            else:
                response = "{\"shop_id\":\"" + m_shop + "\",\"best_cost\":\"" + str(min_sum) + "\"}"
                # if not ex_goods:
                #     response = response+"}"
                # else:
                #     response = response +",\"goods_without_cost\":["
                #     i = 0
                #     for good in ex_goods:
                #         i = i+1
                #         response = response+"\"good_id\":\""+str(good.Good_ID)+"\""
                #         if i !=len(ex_goods):
                #             response=response+","
                #     response = response +"}"

    return status, response

    # end basket methods
