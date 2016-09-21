import sys
import string
from sqlalchemy import Table, MetaData, Column, Integer, String, ForeignKey
from sqlalchemy.orm import mapper, relationship
from sqlalchemy.ext.declarative import declarative_base
metadata = MetaData()

class Good():
    def __init__(self):
        print("init done")

class Basket():
    def __init__(self):
        print("init done")

class User():
    def __init__(self):
        print("init done")

class Shop():
    def __init__(self):
        print("init done")


class City():
    def __init__(self):
        print("init done")

class Region():
    def __init__(self):
        print("init done")

class Baskets():
    def __init__(self):
        print("init done")

class Costs():
    def __init__(self):
        print("init done")