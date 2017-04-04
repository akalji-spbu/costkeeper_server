# -*- coding: utf-8 -*-
import requests
import lxml.html

import anticaptcha

def getGoodInfoByBarcode(barcode):
    url_of_good_page = "https://ean13.info/"+str(barcode)+".htm"
    doc = load_page(url_of_good_page)
    captcha = doc.xpath('/html/body/div/div[2]/div[2]/form')
    attempts = 0
    while captcha:
        attempts = attempts + 1
        anticaptcha.unlock_captcha("6LeCufASAAAAAPVfZ3N-Q6ZHxCx0h5y3s_gGUcYL", "https://ean13.info/tocaptcha.php")
        doc = load_page(url_of_good_page)
        captcha = doc.xpath('/html/body/div/div[2]/div[2]/form')
        if attempts >= 5:
            STATUS = False
            RESPONSE = "A LOT OF CAPTCHA ATTEMPTS"
            return STATUS, RESPONSE


    barcode_xpath = "/html/body/div/div[3]/div/div/div[2]/div[1]/table/tbody/tr[1]/td[2]/small/strong"
    name_xpath = "/html/body/div/div[3]/div/div/div[2]/h1"
    barcode_type_xpath = "/html/body/div/div[3]/div/div/div[2]/div[1]/table/tbody/tr[2]/td[2]/span"
    country_xpath = "/html/body/div/div[3]/div/div/div[2]/div[1]/table/tbody/tr[3]/td[2]/a"
    manufacturer_xpath = "/html/body/div/div[3]/div/div/div[2]/div[1]/table/tbody/tr[4]/td[2]/a"
    picture_uri_xpath = "/html/body/div/div[3]/div/div/div[1]/div/div[3]/p/a"
    description_xpath = "/html/body/div/div[4]/div/div/div[1]/div"
    brand_xpath = "/html/body/div/div[3]/div/div/div[2]/div[1]/table/tbody/tr[5]/td[2]/a"
    category_xpath = "/html/body/div/div[3]/div/div/div[2]/div[1]/table/tbody/tr[7]/td[2]/a"


    name = doc.xpath(name_xpath)[0].text
    if name != "Товар не найден в базе данных":

        barcode = doc.xpath(barcode_xpath)[0].text

        barcode_type = doc.xpath(barcode_type_xpath)[0].text
        country = doc.xpath(country_xpath)[0].text
        manufacturer = doc.xpath(manufacturer_xpath)[0].text
        brand = doc.xpath(brand_xpath)[0].text
        #if doc.xpath(doc.xpath(category_xpath)):
        #    category = doc.xpath(category_xpath)[0].text
        #else:
        category = ""
        if doc.xpath(picture_uri_xpath):
            picture_uri = "https://ean13.info/"+ doc.xpath(picture_uri_xpath)[0].get("href")
        else:
            picture_uri = ""
        if doc.xpath(description_xpath):
            description = doc.xpath(description_xpath)[0].text
        else:
            description = ""

        dataset = {
            "barcode":barcode,
            "name":name,
            "barcode_type":barcode_type,
            "country":country,
            "manufacturer":manufacturer,
            "picture_uri":picture_uri,
            "brand":brand,
            "description":description,
            "category":category
        }
        STATUS = True
        RESPONSE = dataset

    else:
        STATUS = False
        RESPONSE = "GOOD_NOT_FOUND"
    return STATUS, RESPONSE

def load_page(url_of_good_page):
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }
    session = requests.session()
    session.headers = HEADERS
    page = session.get(url_of_good_page)
    doc = lxml.html.document_fromstring(page.text)
    return doc