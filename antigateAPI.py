# -*- coding: utf-8 -*-
import requests
import base64
import config

antigate_generic_API_REQ_URL = config.antigate_generic_API_REQ_URL
antigate_generic_API_RES_URL = config.antigate_generic_API_RES_URL

def send_captcha(captcha_image):
    data = {
        'method':'base64',
        'key': config.antigate_generic_API_KEY,
        'body' : base64.b64encode(captcha_image)
    }
    response = requests.post(antigate_generic_API_REQ_URL, data=data).text
    if response[0:2]=="OK":
        CAPTCHA_ID  = response[3:]
        return CAPTCHA_ID

def check_captcha(CAPTCHA_ID):
    session = requests.session()
    answer = session.get(antigate_generic_API_RES_URL+"?key={}&action=get&id={}".format(config.antigate_generic_API_KEY, CAPTCHA_ID)).text
    return answer

def check_post_exceptions(EXCEPTION):
    if EXCEPTION == "ERROR_WRONG_USER_KEY":
        STATUS = False
        RESPONSE = "ERROR_WRONG_USER_KEY"
    elif EXCEPTION == "ERROR_KEY_DOES_NOT_EXIST":
        STATUS = False
        RESPONSE = "ERROR_KEY_DOES_NOT_EXIST"
    elif EXCEPTION == "ERROR_ZERO_BALANCE":
        STATUS = False
        RESPONSE = "ERROR_ZERO_BALANCE_IN_ANTIGATE_ACCOUNT"
    elif EXCEPTION == "ERROR_NO_SLOT_AVAILABLE":
        STATUS = False
        RESPONSE = "ERROR_NO_SLOT_AVAILABLE"
    elif EXCEPTION == "ERROR_ZERO_CAPTCHA_FILESIZE":
        STATUS = False
        RESPONSE = "ERROR_ZERO_CAPTCHA_FILESIZE"
    elif EXCEPTION == "ERROR_TOO_BIG_CAPTCHA_FILESIZE":
        STATUS = False
        RESPONSE = "ERROR_TOO_BIG_CAPTCHA_FILESIZE"
    elif EXCEPTION == "ERROR_WRONG_FILE_EXTENSION":
        STATUS = False
        RESPONSE = "ERROR_WRONG_FILE_EXTENSION"
    elif EXCEPTION == "ERROR_IMAGE_TYPE_NOT_SUPPORTED":
        STATUS = False
        RESPONSE = "ERROR_IMAGE_TYPE_NOT_SUPPORTED"
    elif EXCEPTION == "ERROR_IP_NOT_ALLOWED":
        STATUS = False
        RESPONSE = "ERROR_IP_NOT_ALLOWED"
    elif EXCEPTION == "IP_BANNED":
        STATUS = False
        RESPONSE = "IP_BANNED"
    elif EXCEPTION == "ERROR_CAPTCHAIMAGE_BLOCKED":
        STATUS = False
        RESPONSE = "ERROR_CAPTCHAIMAGE_BLOCKED"
    else:
        STATUS = False
        RESPONSE = "UNKNOWN ERROR"



    return STATUS, RESPONSE