from selenium import webdriver
import logging
import time
import os
import requests
import random
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common import keys
from retrying import retry
from selenium.webdriver import ActionChains

import pyautogui
pyautogui.PAUSE = 0.5 

logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)



class taobao():
    def __init__(self):
        self.browser = webdriver.Chrome(r'/usr/lib/chromium-browser/chromedriver')
        # 最大化窗口
        self.browser.maximize_window()
        self.browser.implicitly_wait(5)
        self.domain = 'https://www.taobao.com/'
        self.action_chains = ActionChains(self.browser)


    def login(self):
        while True:
            self.browser.get(self.domain)
            time.sleep(1)

            self.browser.find_element_by_xpath('//*[@id="J_SiteNavLogin"]/div[1]/div[1]/a[1]').click()
            time.sleep(1)
            #转为二维码登录
            self.browser.find_element_by_xpath('//*[@id="login"]/div[1]/i').click()

            # Detect if this page is login page
            while self.browser.current_url.startswith("https://login.taobao.com/"):
                print("waiting for user's inputing")
                time.sleep(2)
            print("login successfully!")
            break


    def findImg(self):
        # Find the input and search
        self.browser.find_element_by_xpath('//*[@name="q"]').send_keys("t恤衫", keys.Keys.ENTER)
        time.sleep(2)

        n = 1
        count = 1

        # Create floder
        if not os.path.exists("t恤衫"):
            os.mkdir("t恤衫")

        while True:
            print("count:",count)
            items = self.browser.find_elements_by_css_selector('.m-itemlist .items > div')
            for item in items:
                # get this pic address
                img = item.find_element_by_css_selector(".pic-box .pic img").get_attribute("data-src")
                # full address
                img_url = "http:" + img
                print('img_url:' + img_url)
                sleep_time = random.random() * 10
                time.sleep(sleep_time)
                # download this img by requests
                img_name = f"t恤衫/\\{n}.jpg"
                with open(img_name, 'wb') as file:
                    file.write(requests.get(img_url).content)
                    file.close()
                    print('image%d has downloaded!' % n)
                    time.sleep(1)
                n += 1

            #next page
            self.browser.find_element_by_css_selector('.wraper .items .item.next>a').click()
            time.sleep(10)
            count += 1
            # 100 pages
            if count == 100:
                file.close()
                break

        self.browser.quit()


if __name__ == '__main__':
    tb = taobao()
    tb.login()
    tb.findImg()
    #tb.clear_cart()
