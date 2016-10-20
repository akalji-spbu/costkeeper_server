import config
import costkeeper
from hashlib import md5
from sqlalchemy import TEXT, INTEGER, String

dburi = config.db_dialect + '://' + config.db_user + ':' + config.db_password + '@' + config.db_host + ':' +config.port+ '/'+ config.db_name

def UsersMethods(method,req):
    if (method=="auth"):
        token=user_auth()


def ShopsMethods(method,req):
    return("Hello World")

def GoodsMethods(method,req):
    return("Hello World")

def CostsMethods(method,req):
    return("Hello World")

def BasketsMethods(method,req):
    return("Hello World")



#users methods
def user_check_token(token):
    userid = 1234
    return(userid)


def user_auth(login,password):
    hasher = md5()
    key = config.salt+":"+password
    hasher.update(key)
    passkey = hasher.hexdigest()
    token = ""
    NewUser=costkeeper.User()
    return(token)

def user_reg(login=None,email=None,password=None):
    hasher = md5()
    key = config.salt + ":" + password
    hasher.update(key)
    passkey = hasher.hexdigest()
    token = ""


def user_alter():
    return("Hello World")


def user_delete():
    return("Hello World")


#end users methods