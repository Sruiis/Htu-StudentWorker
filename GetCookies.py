import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions
from aip import AipOcr

URL = "https://htu.g8n.cn/student/course/44867"

STU_ID = "学号"
NAME = '姓名'

APP_ID = "APP_ID"
API_KEY = "API_KEY"
SECRET_KEY = "SECRET_KEY"


# 百度OCR
def baidu_ocr():
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    return client


# 浏览器参数设置
def set_browser():
    options = ChromeOptions()
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")
    browser = webdriver.Chrome(chrome_options=options)
    return options, browser


def work(browser):
    browser.implicitly_wait(30)
    browser.get(url=URL)
    # 输入学号、姓名
    browser.find_element(by=By.NAME, value='no').send_keys(STU_ID)
    browser.find_element(by=By.NAME, value='name').send_keys(NAME)


# 登录
def login(browser, client):
    while True:
        # 保存验证码到本地
        browser.find_element(by=By.XPATH, value='/html/body/div/form/div[3]/div/div/img').screenshot(
            'verifycode_picture.png')
        # 识别验证码
        img = open('verifycode_picture.png', 'rb').read()
        result = client.basicGeneral(img)['words_result'][0]['words']
        # 输入验证码并登录
        verify_code = browser.find_element(by=By.NAME, value='checkcode')
        if len(result) == 4:
            verify_code.send_keys(result)
        verify_code.send_keys(Keys.RETURN)
        if browser.current_url == URL:
            break


# 保存cookies
def save_cookie(browser):
    with open(f'{STU_ID}{NAME}.json', 'w') as f:
        f.write(json.dumps(browser.get_cookies()))


def main():
    options, browser = set_browser()
    work(browser)


if __name__ == "__main__":
    main()
