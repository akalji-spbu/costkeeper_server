import config
import costkeeper
import sqlalchemy.exc
from datetime import datetime
from hashlib import md5
from sqlalchemy import create_engine
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


def user_auth(login,password,email):
    # Creating database session
    engine = create_engine(dburi)
    Session = sessionmaker(bind=engine)
    session = Session()
    # /Creating database session

    hasher = md5()
    key = config.salt+":"+password
    hasher.update(key)
    passkey = hasher.hexdigest()
    token = ""

def user_reg(login=None,email=None,password=None):
    # Creating database session
    engine = create_engine(dburi)
    Session = sessionmaker(bind=engine)
    session = Session()
    # /Creating database session

    key = config.salt + ":" + password
    passkey = md5(key.encode('utf-8')).hexdigest()
    token = ""

    User_Nickname   = login
    User_Email      = email
    User_Firstname  = ""
    User_Lastname   = ""
    Role_ID         = 1
    avatar          = ""
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