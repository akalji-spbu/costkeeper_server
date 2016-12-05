# -*- coding: utf-8 -*-

import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, TEXT, MetaData, ForeignKey, Float, DateTime

Base = declarative_base()


def clrscr():
    try:
        os.system('clear')
    except:
        os.system('cls')


class Good(Base):
    __tablename__ = 'goods'
    Good_ID = Column (Integer, primary_key = True, unique=True)
    Barcode = Column (String(20), unique=True)
    Name = Column (String(45))
    Life = Column (String(45))
    Description = Column (TEXT)
    Prod_country_ID = Column (Integer)
    Type_ID = Column (Integer)
    Picture = Column (String(15))
    def __init__(self, Name, Barcode, Life, Description, Prod_country_ID, Type_ID, Picture):
        self.Name = Name
        self.Life = Life
        self.Barcode = Barcode
        self.Description = Description
        self.Prod_country_ID = Prod_country_ID
        self.Type_ID = Type_ID
        self.Picture = Picture


class Cost(Base):
    __tablename__ = 'costs'
    Cost_Time = Column (DateTime, primary_key = True, unique=True, autoincrement=False)
    Good_ID = Column (Integer)
    Shop_ID = Column (Integer)
    Currency_ID = Column (Integer)
    Cost_value = Column (Float)
    def __init__(self, Cost_Time, Good_ID, Shop_ID, Currency_ID, Cost_value):
        self.Cost_Time = Cost_Time
        self.Good_ID = Good_ID
        self.Shop_ID = Shop_ID
        self.Currency_ID = Currency_ID
        self.Cost_value = Cost_value

class Type_of_good(Base):
    __tablename__ = 'types_of_goods'
    Type_ID = Column (Integer, primary_key = True, unique=True)
    Name = Column (String(45))
    def __init__(self, Name):
        self.Name = Name


class Currency(Base):
    __tablename__ = 'currency'
    Currency_ID = Column (Integer, primary_key = True, unique=True)
    Name = Column (String(45))
    Code = Column (String(5), unique=True)
    def __init__(self, Name, Code):
        self.Name = Name
        self.Code = Code


class Basket(Base):
    __tablename__ = 'baskets'
    Basket_ID  = Column (Integer, primary_key = True, unique=True)
    User_ID = Column (Integer)
    Creation_date = Column (DateTime)
    Modify_date = Column (DateTime)
    Name = Column (String(45))
    def __init__(self, User_ID, Creation_date, Modify_date, Name):
        self.User_ID = User_ID
        self.Creation_date = Creation_date
        self.Modify_date = Modify_date
        self.Name = Name


class Good_in_basket(Base):
    __tablename__ = 'goods_in_baskets'
    Basket_ID = Column (Integer, primary_key = True, autoincrement=False)
    Good_ID = Column (Integer, primary_key = True, autoincrement=False)
    Number_of_goods = Column(Integer)
    def __init__(self, Basket_ID, Good_ID, Number_of_goods):
        self.Basket_ID = Basket_ID
        self.Good_ID = Good_ID
        self.Number_of_goods = Number_of_goods


class Country(Base):
    __tablename__               = 'countries'
    Сountry_ID                  = Column(Integer, primary_key=True, unique=True)
    Сountry_Name                = Column(String(45))
    def __init__(self, Сountry_Name):
        self.Country_Name       = Сountry_Name


class Region(Base):
    __tablename__               = 'regions'
    Region_ID                   = Column(Integer, primary_key=True, unique=True)
    Region_Name                 = Column(String(45))
    countries_Country_ID                 = Column(Integer)
    def __init__(self, Region_Name, Сountry_ID):
        self.Region_Name       = Region_Name
        self.countries_Country_ID         = Сountry_ID


class City(Base):
    __tablename__               = 'cities'
    City_ID                     = Column(Integer, primary_key=True, unique=True)
    City_Name                   = Column(String(45))
    regions_Region_ID                   = Column(Integer)
    def __init__(self, City_Name, Region_ID):
        self.City_Name          = City_Name
        self.regions_Region_ID          = Region_ID


class Street(Base):
    __tablename__               = 'streets'
    Street_ID                   = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    Street_Name                 = Column(String(45))
    def __init__(self, Street_Name):
        self.Street_Name        = Street_Name



class User(Base):
    __tablename__               = 'users'
    User_ID                     = Column(Integer, primary_key=True, unique=True)
    User_Nickname               = Column(String(45))
    User_Email                  = Column(String(45))
    User_Firstname              = Column(String(45))
    User_Lastname               = Column(String(45))
    Role_ID                     = Column(Integer)
    avatar                      = Column(String(45))
    password                    = Column(String(45))
    token                       = Column(String(45))
    token_lifetime              = Column(DateTime)
    Creation_Date               = Column(DateTime)

    def __init__(self, User_Nickname, User_Email, User_Firstname, User_Lastname, Role_ID, avatar, password, token, token_lifetime,Creation_Date):
        self.User_Nickname      = User_Nickname
        self.User_Email         = User_Email
        self.User_Firstname     = User_Firstname
        self.User_Lastname      = User_Lastname
        self.Role_ID            = Role_ID
        self.avatar             = avatar
        self.password           = password
        self.token              = token
        self.token_lifetime     = token_lifetime
        self.Creation_Date      = Creation_Date

class Role(Base):
    __tablename__               = 'roles'
    Role_ID                     = Column(Integer, primary_key=True, unique=True)
    Role_Name                   = Column(String(45))
    admin                       = Column(Integer)
    def __init__(self, Role_Name, admin):
        self.Role_Name          = Role_Name
        self.admin              = admin


class Shop(Base):
    __tablename__ = 'shops'
    Shop_ID                     = Column(Integer, primary_key=True, unique=True)
    Shop_Name                   = Column(String(45))
    City_ID                     = Column(Integer)
    Street_ID                   = Column(Integer)
    Building                    = Column(String(45))
    def __init__(self, Shop_Name, City_ID, Street_ID, Building):
        self.Shop_Name          = Shop_Name
        self.City_ID            = City_ID
        self.Street_ID          = Street_ID
        self.Building           = Building
