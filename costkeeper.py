import sys
import string
import os
import config
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, create_engine

Base = declarative_base()

def clrscr():
    try:
        os.system('clear')
    except:
        os.system('cls')

class Bountry(Base):
    __tablename__ = 'countries'
    Сountry_ID = Column(Integer, primary_key=True)