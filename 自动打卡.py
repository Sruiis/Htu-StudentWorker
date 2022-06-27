import time
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from aip import AipOcr

if __name__ == "__main__":
    URL = "https://htu.g8n.cn/student/course/44867"

    STU_ID = '学号'
    NAME = '姓名'

    # 百度OCR
    APP_ID = ''
    API_KEY = ''
    SECRET_KEY = ''
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    # 浏览器参数设置
    options = Options()
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")
    browser = webdriver.Chrome(chrome_options=options)

    browser.get(url=URL)
    # 输入学号、姓名
    browser.find_element_by_name('no').send_keys(STU_ID)
    browser.find_element_by_name('name').send_keys(NAME)

    # 登录
    while True:
        # 保存验证码到本地
        browser.find_element_by_xpath('/html/body/div/form/div[3]/div/div/img').screenshot('verifycode_picture.png')
        # 识别验证码
        img = open('verifycode_picture.png', 'rb').read()
        result = client.basicGeneral(img)['words_result'][0]['words']
        # 输入验证码并登录
        verify_code = browser.find_element_by_name('checkcode')
        if len(result) == 4:
            verify_code.send_keys(result)
        verify_code.send_keys(Keys.RETURN)
        if browser.current_url == URL:
            break

    # 保存cookies
    with open('cookies.json', 'w') as f:
        f.write(json.dumps(browser.get_cookies()))

