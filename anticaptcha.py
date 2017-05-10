# -*- coding: utf-8 -*-
def unlock_captcha(captcha_api_key, captcha_url):
    import re
    import requests
    from time import sleep
    import antigateAPI
    import config

    session = requests.session()
    challenge_uri = "http://www.google.com/recaptcha/api/challenge?k=" + captcha_api_key
    challenge_text = session.get(challenge_uri).text
    regex = r"'([^']+)'"
    matches = re.search(regex, challenge_text)
    if matches:
        challange_session_id = matches.group()[1:-1]

    challange_image_uri = "https://www.google.com/recaptcha/api/image?c=" + challange_session_id
    captcha_image = session.get(challange_image_uri).content
    captcha_answer = ""

    if config.anticaptha_mode == "ANTIGATE":
        print("ANTIGATE")
        CAPTCHA_ID = antigateAPI.send_captcha(captcha_image)
        captcha_answer = antigateAPI.check_captcha(CAPTCHA_ID)
        while 'CAPCHA_NOT_READY' in captcha_answer:
            sleep(5)
            captcha_answer = antigateAPI.check_captcha(CAPTCHA_ID)
        if captcha_answer[0:2] == "OK":
            captcha_answer = captcha_answer[3:]
        else:
            STATUS, RESPONSE = antigateAPI.check_post_exceptions(captcha_answer)
            if STATUS == False:
                return RESPONSE
            if STATUS == True:
                return

    if config.anticaptha_mode == "MANUAL":
        print(challange_image_uri)
        captcha_answer = input('Ответ: ')

    data = {'recaptcha_response_field': captcha_answer,
            'recaptcha_challenge_field': challange_session_id
            }
    requests.post(captcha_url, data=data)

