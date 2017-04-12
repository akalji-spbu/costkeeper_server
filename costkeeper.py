# -*- coding: utf-8 -*-

import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table,Boolean, Column, Integer, String, TEXT, MetaData, ForeignKey, Float, DateTime

Base = declarative_base()


def clrscr():
    try:
        os.system('clear')
    except:
        os.system('cls')


class Cost(Base):
    __tablename__ = 'costs'

    Cost_Time   = Column (DateTime, primary_key = True, unique=True, autoincrement=False)
    Good_ID     = Column (Integer)
    Shop_ID     = Column (Integer)
    Currency_ID = Column (Integer)
    Cost_Value  = Column (Float)

    def __init__(self, Cost_Time, Good_ID, Shop_ID, Currency_ID, Cost_Value):
        self.Cost_Time   = Cost_Time
        self.Good_ID     = Good_ID
        self.Shop_ID     = Shop_ID
        self.Currency_ID = Currency_ID
        self.Cost_Value  = Cost_Value

class Currency(Base):
    __tablename__ = 'currency'

    Currency_ID = Column (Integer, primary_key = True, unique=True)
    Name        = Column (String(45))
    Code        = Column (String(5), unique=True)

    def __init__(self, Name, Code):
        self.Name = Name
        self.Code = Code


class Good(Base):
    __tablename__ = 'goods'

    Good_ID     = Column (Integer, primary_key = True, unique=True)
    Barcode     = Column (String(20), unique=True)
    Name        = Column (String(45))
    Life        = Column (String(45))
    Description = Column (TEXT)
    Type_ID     = Column (Integer)
    Units_ID    = Column (Integer)
    Alcohol     = Column (Boolean)
    Brand       = (String(45))

    def __init__(self, Name, Barcode, Life, Description, Type_ID, Units_ID, Alcohol, Brand):
        self.Name        = Name
        self.Life        = Life
        self.Barcode     = Barcode
        self.Description = Description
        self.Type_ID     = Type_ID
        self.Units_ID    = Units_ID
        self.Alcohol     = Alcohol
        self.Brand       = Brand

class Type_of_good(Base):
    __tablename__ = 'types_of_goods'

    Type_ID        = Column (Integer, primary_key = True, unique=True)
    Name           = Column (String(45))
    Parent_Type_ID = Column (Integer)

    def __init__(self, Name, Parent_Type_ID):
        self.Name           = Name
        self.Parent_Type_ID = Parent_Type_ID


class Manufacturer(Base):
    __tablename__ = 'manufacturers'

    Manufacturer_ID            = Column (Integer, primary_key = True, unique=True)
    Manufacturer_Name          = Column (String(30))
    Manufacturer_Original_Name = Column (String(30))
    Country_ID                 = Column (Integer)

    def __init__(self, Manufacturer_ID, Manufacturer_Name, Manufacturer_Original_Name, Country_ID):
        self.Manufacturer_ID            = Manufacturer_ID
        self.Manufacturer_Name          = Manufacturer_Name
        self.Manufacturer_Original_Name = Manufacturer_Original_Name
        self.Country_ID                 = Country_ID

class Unit(Base):
    __tablename__ = 'units'

    Name                     = Column (String(45))
    International_Name       = Column (String(45))
    Short_Name               = Column (String(5))
    International_Short_Name = Column (String(5))

    def __init__(self, Name, International_Name, Short_Name, International_Short_Name):
        self.Name                     = Name
        self.International_Name       = International_Name
        self.Short_Name               = Short_Name
        self.International_Short_Name = International_Short_Name

class Alcohol(Base):
    __tablename__ = 'alcohol'

    Good_ID             = Column (Integer)
    Strength_Of_Alcohol = Column (String(5))
    Type_Of_Alcohol     = Column (Integer)

    def __init__(self, Good_ID, Strength_Of_Alcohol, Type_Of_Alcohol):
        self.Good_ID             = Good_ID
        self.Strength_Of_Alcohol = Strength_Of_Alcohol
        self.Type_Of_Alcohol     = Type_Of_Alcohol

class Type_of_alcohol(Base):
    __tablename__ = 'types_of_alcohol'

    Type_ID            = Column (Integer, primary_key = True, unique=True)
    Name               = Column (String(45))
    International_Name = Column (String(45))

    def __init__(self, Type_ID, Name, International_Name):
        self.Type_ID            = Type_ID
        self.Name               = Name
        self.International_Name = International_Name

class Additional_good_picture(Base):
    __tablename__ = 'additional_good_pictures'

    Picture_ID = Column (Integer, primary_key = True, unique=True)
    Good_ID    = Column (Integer)

    def __init__(self, Picture_ID, Good_ID):
        self.Picture_ID = Picture_ID
        self.Good_ID    = Good_ID


class Basket(Base):
    __tablename__ = 'baskets'

    Basket_ID     = Column (Integer, primary_key = True, unique=True)
    User_ID       = Column (Integer)
    Creation_Date = Column (DateTime)
    Modify_Date   = Column (DateTime)
    Name = Column (String(45))

    def __init__(self, User_ID, Creation_Date, Modify_Date, Name):
        self.User_ID       = User_ID
        self.Creation_Date = Creation_Date
        self.Modify_Date   = Modify_Date
        self.Name          = Name

class Good_in_basket(Base):
    __tablename__ = 'goods_in_baskets'

    Basket_ID       = Column (Integer, primary_key = True, autoincrement=False)
    Good_ID         = Column (Integer, primary_key = True, autoincrement=False)
    Number_Of_Goods = Column(Integer)

    def __init__(self, Basket_ID, Good_ID, Number_Of_Goods):
        self.Basket_ID       = Basket_ID
        self.Good_ID         = Good_ID
        self.Number_Of_Goods = Number_Of_Goods


class Country(Base):
    __tablename__ = 'countries'

    Сountry_ID   = Column(Integer, primary_key=True, unique=True)
    Сountry_Name = Column(String(45))

    def __init__(self, Сountry_Name):
        self.Country_Name = Сountry_Name

class Region(Base):
    __tablename__ = 'regions'

    Region_ID    = Column(Integer, primary_key=True, unique=True)
    Region_Name  = Column(String(45))
    Country_ID   = Column(Integer)

    def __init__(self, Region_Name, Сountry_ID):
        self.Region_Name = Region_Name
        self.Country_ID  = Сountry_ID

class City(Base):
    __tablename__ = 'cities'

    City_ID     = Column(Integer, primary_key=True, unique=True)
    City_Name   = Column(String(45))
    Region_ID   = Column(Integer)

    def __init__(self, City_Name, Region_ID):
        self.City_Name = City_Name
        self.Region_ID = Region_ID

class Street(Base):
    __tablename__ = 'streets'

    Street_ID   = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    Street_Name = Column(String(45))

    def __init__(self, Street_Name):
        self.Street_Name = Street_Name


class User(Base):
    __tablename__ = 'users'

    User_ID         = Column(Integer, primary_key=True, unique=True)
    User_Nickname   = Column(String(45))
    User_Email      = Column(String(45))
    User_Firstname  = Column(String(45))
    User_Lastname   = Column(String(45))
    Role_ID         = Column(Integer)
    Password        = Column(String(45))
    Token           = Column(String(45))
    Token_Lifetime  = Column(DateTime)
    Creation_Date   = Column(DateTime)

    def __init__(self, User_Nickname, User_Email, User_Firstname, User_Lastname, Role_ID, Password, Token, Token_Lifetime,Creation_Date):
        self.User_Nickname   = User_Nickname
        self.User_Email      = User_Email
        self.User_Firstname  = User_Firstname
        self.User_Lastname   = User_Lastname
        self.Role_ID         = Role_ID
        self.Password        = Password
        self.Token           = Token
        self.Token_Lifetime  = Token_Lifetime
        self.Creation_Date   = Creation_Date

class Role(Base):
    __tablename__  = 'roles'

    Role_ID    = Column(Integer, primary_key=True, unique=True)
    Role_Name  = Column(String(45))
    Admin      = Column(Boolean)

    def __init__(self, Role_Name, Admin):
        self.Role_Name = Role_Name
        self.Admin     = Admin


class Shop(Base):
    __tablename__ = 'shops'

    Shop_ID    = Column(Integer, primary_key=True, unique=True)
    Shop_Name  = Column(String(45))
    City_ID    = Column(Integer)
    Street_ID  = Column(Integer)
    Building   = Column(String(45))

    def __init__(self, Shop_Name, City_ID, Street_ID, Building):
        self.Shop_Name  = Shop_Name
        self.City_ID    = City_ID
        self.Street_ID  = Street_ID
        self.Building   = Building
