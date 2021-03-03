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

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)



class jingdong():
    def __init__(self):
        #webdriver位置
        self.browser = webdriver.Chrome(r'/usr/lib/chromium-browser/chromedriver')
        # 最大化窗口
        self.browser.maximize_window()
        self.browser.implicitly_wait(5)
        #爬取网站首页地址
        self.domain = 'https://www.jd.com/'
        self.action_chains = ActionChains(self.browser)

    def login(self):
        while True:
            self.browser.get(self.domain)
            time.sleep(1)

            #模拟点击登录
            self.browser.find_element_by_xpath('//*[@id="ttbar-login"]/a[1]').click()
            time.sleep(1)

            #判断是否还在登录页面
            while self.browser.current_url.startswith("https://passport.jd.com/"):
                print("waiting for user's inputing")
                time.sleep(2)
            print("login successfully!")
            break

    def findImg(self):
        #找到输入框并搜索关键词
        self.browser.find_element_by_xpath('//*[@id="key"]').send_keys("t恤衫", keys.Keys.ENTER)
        time.sleep(2)

        n = 1
        count = 1

        #保存图片的文件夹
        if not os.path.exists("t恤衫"):
            os.mkdir("t恤衫")

        while True:
            print("count:", count)
            items = self.browser.find_elements_by_css_selector('.gl-warp.clearfix .gl-item > div')
            for item in items:
                # 由于京东商品显示是动态加载的，因此每次下载都将滚动条调整至该图片所在位置
                self.browser.execute_script("arguments[0].scrollIntoView();",item)
                time.sleep(1)
                # 找到图片地址
                img = item.find_element_by_css_selector(".p-img img").get_attribute("src")
                print(img)
                # 完整的图片地址
                img_url = img
                print('img_url:' + img_url)
                sleep_time = random.random() * 10
                time.sleep(sleep_time)
                # 下载图片
                img_name = f"t恤衫{n}.jpg"
                with open(img_name, 'wb') as file:
                    file.write(requests.get(img_url).content)
                    file.close()
                    print('image%d has downloaded!' % n)
                    time.sleep(1)
                n += 1

            # 找到下一页按钮，并点击
            self.browser.find_element_by_css_selector('.p-wrap .p-num .pn-next').click()
            time.sleep(5)
            count += 1
            # 100 pages
            if count == 100:
                break

        self.browser.quit()


if __name__ == '__main__':
    jd = jingdong()
    jd.login()
    jd.findImg()