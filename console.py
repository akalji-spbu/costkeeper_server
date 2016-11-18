# -*- coding: utf-8 -*-

import config
import costkeeper
from xml.dom.minidom import parse
import xml.dom.minidom
import sqlalchemy.exc
import random
import string
import datetime
from datetime import datetime, timedelta
from hashlib import md5
from sqlalchemy import create_engine, select, delete
from sqlalchemy.sql import table, column
from sqlalchemy.orm import sessionmaker
from sqlalchemy import TEXT, INTEGER, String

dburi = config.db_dialect + '://' + config.db_user + ':' + config.db_password + '@' + config.db_host + ':' +config.db_port+ '/'+ config.db_name +'?charset=utf8'

costkeeper.clrscr()

def import_regions():
    PATH = "cities.xml"
    DOMTree = xml.dom.minidom.parse(PATH)
    collection = DOMTree.documentElement
    countryID = "1"
    cities = collection.getElementsByTagName("city")
    for city in cities:
        engine = create_engine(dburi)
        conn = engine.connect()
        Session = sessionmaker(bind=engine)
        session = Session()
        our_region = city.getAttribute("part")
        city.getElementsByTagName('city')
        our_city = city.childNodes[0].data
        if (our_region == ""):
            our_region = "без региона"
        select_stmt = select([costkeeper.Region.Region_ID]).where(costkeeper.Region.Region_Name == our_region)
        result = conn.execute(select_stmt)
        rows = result.fetchall()
        result.close()
        if not rows:
            NewRegion = costkeeper.Region(our_region,countryID)
            session.add(NewRegion)
            session.commit()
        session.close()



def import_cities():
    PATH = input("path of XML with cities: ")
    PATH = "cities.xml"
    DOMTree = xml.dom.minidom.parse(PATH)
    collection = DOMTree.documentElement
    countryID = "1"
    cities = collection.getElementsByTagName("city")
    for city in cities:
        engine = create_engine(dburi)
        conn = engine.connect()
        Session = sessionmaker(bind=engine)
        session = Session()
        our_region = city.getAttribute("part")
        city.getElementsByTagName('city')
        our_city = city.childNodes[0].data
        if(our_region==""):
            our_region="без региона"
        select_stmt = select([costkeeper.Region.Region_ID]).where(costkeeper.Region.Region_Name == our_region)
        result = conn.execute(select_stmt)
        rowsregion = result.fetchall()
        result.close()
        select_stmt = select([costkeeper.City.City_ID]).where(costkeeper.City.City_Name == our_city)
        result = conn.execute(select_stmt)
        rows = result.fetchall()
        result.close()
        if not rows:
            NewCity = costkeeper.City(our_city, int(rowsregion[0].Region_ID))
            session.add(NewCity)
            session.commit()
        session.close()





import_cities()