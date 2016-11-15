import config
import costkeeper
import sqlalchemy.exc
import random
import string
from datetime import datetime, timedelta
from hashlib import md5
from sqlalchemy import create_engine, select
from sqlalchemy.sql import table, column
from sqlalchemy.orm import sessionmaker
from sqlalchemy import TEXT, INTEGER, String

dburi = config.db_dialect + '://' + config.db_user + ':' + config.db_password + '@' + config.db_host + ':' +config.db_port+ '/'+ config.db_name


#users methods
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
        response = "TOKEN_DOES_NOT_EXIST"
    else:
        if (rows[0].token_lifetime < datetime.today()):
            response = "TOKEN_EXSPIRED"
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
        print("Error adding")

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
        return "TOKEN_DOES_NOT_EXIST"
    else:
        select_stmt = select([costkeeper.User.token_lifetime]).where(costkeeper.User.token == token)
        result = conn.execute(select_stmt)
        rows = result.fetchall()
        result.close()
        if not rows:
            return "TOKEN_DOES_NOT_EXIST"
        if(rows[0].token_lifetime < datetime.today()):
            return "TOKEN_EXSPIRED"
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
    return "Success"


def user_delete():
    # Creating database session
    engine = create_engine(dburi)
    Session = sessionmaker(bind=engine)
    session = Session()
    # /Creating database session
    return("Hello World")

def user_alter_password(token="",password="",newpassword=""):
    # Creating database session
    engine = create_engine(dburi)
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    # /Creating database session
    if(len(token) == 0):
        return "TOKEN_DOES_NOT_EXIST"
    else:
        key = config.salt + ":" + password
        passkey = md5(key.encode('utf-8')).hexdigest()
        select_stmt = select([costkeeper.User.token_lifetime,costkeeper.User.password]).where(costkeeper.User.token == token)
        result = conn.execute(select_stmt)
        rows = result.fetchall()
        result.close()
        if not rows:
            return "TOKEN_DOES_NOT_EXIST"
        if(rows[0].token_lifetime < datetime.today()):
            return "TOKEN_EXSPIRED"
        if(rows[0].password !=passkey):
            return "WRONG_PASSWORD"
        key = config.salt + ":" + newpassword
        passkey = md5(key.encode('utf-8')).hexdigest()
        ourUser = session.query(costkeeper.User).filter_by(token=token).first()
        ourUser.password = passkey
        a = string.ascii_lowercase + string.digits
        token = ''.join([random.choice(a) for i in range(20)])
        ourUser.token = token
        ourUser.token_lifetime = datetime.today()+timedelta(days=1)
        session.commit()
        return token


def user_get(token="",ID="",secret=""):
    # Creating database session
    engine = create_engine(dburi)
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    # /Creating database session
    if (len(token) == 0):
        return "TOKEN_DOES_NOT_EXIST"
    else:
        select_stmt = select([costkeeper.User.token_lifetime]).where(costkeeper.User.token == token)
        result = conn.execute(select_stmt)
        rows = result.fetchall()
        result.close()
        if not rows:
            return "TOKEN_DOES_NOT_EXIST"
        if (rows[0].token_lifetime < datetime.today()):
            return "TOKEN_EXSPIRED"
        select_stmt = select([costkeeper.User.User_ID,costkeeper.User.User_Nickname,costkeeper.User.User_Firstname,costkeeper.User.User_Lastname,costkeeper.User.avatar ]).where(costkeeper.User.User_ID == ID)
        result = conn.execute(select_stmt)
        rows = result.fetchall()
        result.close()
        if not rows:
            return "USER_DOES_NOT_EXIST"
        json_data = '{"user_id":"'+str(rows[0].User_ID) +'","nickname": "'+rows[0].User_Nickname +'","firstname":"'+ rows[0].User_Firstname+'","lastname":"'+rows[0].User_Lastname +'","avatar": "'+rows[0].avatar +'"}'
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
        except sqlalchemy.exc.OperationalError:
            response = "ADDING_ERROR"
            status   = False

        session.commit()

    else:
        status = False
        response = "SHOP_ALREDY_EXIST"


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
        return "SHOP_DOES_NOT_EXIST"
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
        return "SHOP_DOES_NOT_EXIST"
    else:
        json_data = '{"shop_id":"'+str(rows[0].Shop_ID) +'","name": "'+rows[0].Shop_Name +'","city_id":"'+ rows[0].City_ID+'","street_id":"'+rows[0].Street_ID +'","building": "'+rows[0].Building +'"}'
        return json_data

#end shops methods

#good methods
def good_exist(good_id=""):
    status = True
    # Creating database session
    engine = create_engine(dburi)
    conn = engine.connect()
    # /Creating database session

    select_stmt = select([costkeeper.Good.Good_ID]).where(costkeeper.Good.Good_ID == id)
    result = conn.execute(select_stmt)
    rows = result.fetchall()
    result.close()

    if not rows:
        status = False
    return status

def good_add(barcode=0, name="", life="", description="", prod_country_id="", type_id="", picture=""):
    # Creating database session
    engine = create_engine(dburi)
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    # /Creating database session
    status = True
    response ="SUCCESS"

    select_stmt = select([costkeeper.Good.Good_ID]).where(costkeeper.Good.Barcode == barcode)
    result = conn.execute(select_stmt)
    rows = result.fetchall()
    result.close()

    if not rows:
        newGood = costkeeper.Good(barcode, name, life, description, prod_country_id, type_id, picture)
        try:
            session.add(newGood)
        except sqlalchemy.exc.OperationalError:
            status = False
            response = "ADDING_ERROR"
    else:
        status = False
        response = "GOOD_ALREADY_EXIST"

    session.commit()
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

    check_good = good_exist(id)
    if check_good == True:
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
    else:
        status = False
        response = "GOOD_DOES_NOT_EXIST"

    session.commit()
    return status, response

def good_get(secret="", good_id=""):
    # Creating database session
    engine = create_engine(dburi)
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    # /Creating database session
    status = True
    response = "SUCCESS"

    status = good_exist(good_id)
    if status == True:
        select_stmt = select([costkeeper.Good.Good_ID, costkeeper.Good.Barcode, costkeeper.Good.Life, costkeeper.Good.Description,
                              costkeeper.Good.Name, costkeeper.Good.Picture, costkeeper.Good.Prod_county_ID ]).where(costkeeper.Good.Good_ID == good_id)
        result = conn.execute(select_stmt)
        rows = result.fetchall()
        result.close()
        response = '{"good_id":"'+str(rows[0].Good_ID) +'","barecode": "'+rows[0].Barecode +'","life": "'+rows[0].Life +'","description": "'+rows[0].Description \
                   +'","name": "'+rows[0].Name +'","picture": "'+rows[0].Picture +'","prod_country_id": "'+rows[0].Prod_country_ID +'","type_id": "'+rows[0].Type+'"}'
    else:
        response = "GOOD_DOES_NOT_EXIST"
    return status, response

def good_get_cost(secret="", good_id="", shop_id=""):
    # Creating database session
    engine = create_engine(dburi)
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    # /Creating database session
    status = True
    response = "SUCCESS"
    return status, response

def good_get_costs_in_all_shops(secret="", good_id=""):
    # Creating database session
    engine = create_engine(dburi)
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    # /Creating database session
    status = True
    response = "SUCCESS"
    return status, response

def good_get_cost_history_in_shop(secret="", good_id="", shop_id=""):
    # Creating database session
    engine = create_engine(dburi)
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    # /Creating database session
    status = True
    response = "SUCCESS"
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