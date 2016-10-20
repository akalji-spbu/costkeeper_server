import sys
import string
import os
import config
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, TEXT, MetaData, ForeignKey, create_engine, Float

Base = declarative_base()


def clrscr():
    try:
        os.system('clear')
    except:
        os.system('cls')


class Good(Base):
    __tablename__ = 'goods'
    Good_ID = Column (Integer, primary_key = True)
    Barcode = Column (Integer)
    Name = Column (String(45))
    Life = Column (String(45))
    Description = Column (TEXT)
    Prod_county_ID = Column(Integer)
    Type_ID = Column (Integer)
    Picture = Column (String(15))
    def __init__(self, Goog_ID, Name, Life, Description, Prod_country_ID, Type_ID):
        self.Good_ID = Goog_ID
        self.Name = Name
        self.Life = Life
        self.Description = Description
        self.Prod_county_ID = Prod_country_ID
        self.Type_ID = Type_ID


class Cost(Base):
    __tablename__ = 'costs'
    Cost_ID = Column (Integer,primary_key = True)
    Good_ID = Column (Integer)
    Shop_ID = Column (Integer)
    Currency_ID = Column (Integer)
    Cost_value = Column (Float)
    def __init__(self, Cost_ID, Good_ID, Shop_ID, Currency_ID, Cost_value):
        self.Cost_ID = Cost_ID
        self.Good_ID = Good_ID
        self.Shop_ID = Shop_ID
        self.Currency_ID = Currency_ID
        self.Cost_value = Cost_value


class Type_of_good(Base):
    __tablename__ = 'types_of_goods'
    Type_ID = Column (Integer, primary_key = True)
    Name = Column (String(20))
    def __init__(self, Type_ID, Name):
        self.Type_ID = Type_ID
        self.Name = Name


class Currency(Base):
    __tablename__ = 'currency'
    Currency_ID = Column (Integer, primary_key = True)
    Name = Column (String(20))
    Code = Column (String(5))
    def __init__(self, Currency_ID, Name, Code):
        self.Currency_ID = Currency_ID
        self.Name = Name
        self.Code = Code


class Basket(Base):
    __tablename__ = 'basket'
    Basket_ID  = Column (Integer, primary_key = True)
    User_ID = Column (Integer)
    Creation_date = Column (Integer)
    Modify_date = Column (Integer)
    Name = Column (String(20))
    def __init__(self, Basket_ID, User_ID, Creation_date, Modify_date, Name):
        self.Basket_ID = Basket_ID
        self.User_ID = User_ID
        self.Creation_date = Creation_date
        self.Modify_date = Modify_date
        self.Name = Name


class Good_in_basket(Base):
    __tablename__ = 'Goods_in_baskets'
    Basket_ID = Column (Integer, primary_key = True)
    Good_ID = Column (Integer)
    Number_of_goods = Column(Integer)
    def __init__(self, Basket_ID, Good_ID, Number_of_goods):
        self.Basket_ID = Basket_ID
        self.Good_ID = Good_ID
        self.Number_of_goods = Number_of_goods


class Country(Base):
    __tablename__               = 'countries'
    Сountry_ID                  = Column(Integer, primary_key=True)
    Сountry_Name                = Column(String(20))
    def __init__(self, Сountry_ID, Сountry_Name):
        self.Сountry_ID         = Сountry_ID
        self.Country_Name       = Сountry_Name


class Region(Base):
    __tablename__               = 'regions'
    Region_ID                   = Column(Integer, primary_key=True)
    Region_Name                 = Column(String(20))
    Region_Code                 = Column(Integer)
    def __init__(self, Сountry_ID, Сountry_Name, Country_ID):
        self.Сountry_ID         = Сountry_ID
        self.Country_Name       = Сountry_Name
        self.Country_ID         = Country_ID


class City(Base):
    __tablename__               = 'cities'
    City_ID                     = Column(Integer, primary_key=True)
    City_Name                   = Column(String(20))
    Region_ID                   = Column(Integer)
    def __init__(self, City_ID, City_Name, Region_ID):
        self.City_ID            = City_ID
        self.City_Name          = City_Name
        self.Region_ID          = Region_ID


class Street(Base):
    __tablename__               = 'streets'
    Street_ID                   = Column(Integer, primary_key=True)
    Street_Name                 = Column(String(20))
    def __init__(self, Street_ID, Street_Name):
        self.Street_ID          = Street_ID
        self.Street_Name        = Street_Name



class User(Base):
    __tablename__               = 'users'
    User_ID                     = Column(Integer, primary_key=True)
    User_Nickname               = Column(String(20))
    User_Email                  = Column(String(20))
    User_Firstname              = Column(String(20))
    User_Lastname               = Column(String(20))
    Role_ID                     = Integer
    avatar                      = Column(String(20))
    password                    = Column(String(20))
    def __init__(self, User_ID, User_Nickname, User_Email, User_Firstname, User_Lastname, Role_ID, avatar, password):
        self.User_ID            = User_ID
        self.User_Nickname      = User_Nickname
        self.User_Email         = User_Email
        self.User_Firstname     = User_Firstname
        self.User_Lastname      = User_Lastname
        self.Role_ID            = Role_ID
        self.avatar             = avatar
        self.password           = password


class Role(Base):
    __tablename__               = 'roles'
    Role_ID                     = Column(Integer, primary_key=True)
    Role_Name                   = Column(String(20))
    admin                       = Column(Integer)
    def __init__(self, Role_ID, Role_Name, admin):
        self.Role_ID            = Role_ID
        self.Role_Name          = Role_Name
        self.admin              = admin


class Shop(Base):
    __tablename__ = 'shops'
    Shop_ID                     = Column(Integer, primary_key=True)
    Shop_Name                   = Column(String(20))
    City_ID                     = Column(Integer)
    Street_ID                   = Column(Integer)
    Building                    = Column(String(20))
    def __init__(self, Shop_ID, Shop_Name, City_ID, Street_ID, Building):
        self.Shop_ID            = Shop_ID
        self.Shop_Name          = Shop_Name
        self.City_ID            = City_ID
        self.Street_ID          = Street_ID
        self.Building           = Building
