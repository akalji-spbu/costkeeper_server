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
def shop_add():
    print()

def shop_alter():
    print()

def shop_complaint():
    print()

def shop_get():
    print()

#end shops methods

#good methods



#end good methods