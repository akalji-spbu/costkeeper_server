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
    Session = sessionmaker(bind=engine)
    session = Session()
    # /Creating database session
    userid = 1234
    return(userid)

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


def user_alter():
    # Creating database session
    engine = create_engine(dburi)
    Session = sessionmaker(bind=engine)
    session = Session()
    # /Creating database session
    return("Hello World")


def user_delete():
    # Creating database session
    engine = create_engine(dburi)
    Session = sessionmaker(bind=engine)
    session = Session()
    # /Creating database session
    return("Hello World")

def user_alter_password():
    # Creating database session
    engine = create_engine(dburi)
    Session = sessionmaker(bind=engine)
    session = Session()
    # /Creating database session
    return ("Hello World")

def user_get():
    # Creating database session
    engine = create_engine(dburi)
    Session = sessionmaker(bind=engine)
    session = Session()
    # /Creating database session
    return ("Hello World")


#end users methods


#shops methods

#end shops methods