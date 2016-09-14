import sys
import string
from datetime import datetime
from xml.dom.minidom import parse
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Good(Base):
    def __init__(self):
        print("init done")

class Basket(Base):
    def __init__(self):
        print("init done")

class User(Base):
    def __init__(self):
        print("init done")

class Shops(Base):
    def __init__(self):
        print("init done")

