from sqlalchemy import TEXT, INTEGER, String

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


def user_auth():
    return("Hello World")


def user_alter():
    return("Hello World")


def user_delete():
    return("Hello World")


#end users methods