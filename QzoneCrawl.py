# -*- coding:utf-8 -*-

import re
import codecs
from bs4 import BeautifulSoup
from selenium import webdriver
import time


class QzoneSpider(object):
    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.pattern = re.compile(r'src="(\S+)"')

    def get_AD_info(self, driver):
        print "enter get_AD_info"
        driver.switch_to_default_content()
        while True:
            try:
                js = "window.scrollTo(0, document.body.scrollHeight);"
                driver.execute_script(js)
                time.sleep(5)
            except Exception, e:
                print e
                break
            htm_const = driver.page_source
            soup = BeautifulSoup(htm_const, features='lxml')

            ad_info = soup.find_all(name="div", attrs={"class": "f-single-content f-wrap"})
            file = codecs.open(u'广告' + u'.txt', 'a', 'utf-8')
            for info in ad_info:
                ad = info.find(class_="f-single-top")
                if ad:
                    file.write('--' * 45)
                    file.write('\r\n')
                    ad_title = info.select("div > div.class#f-info")
                    print ad_title
                    if ad_title:
                        ad_title = ad_title.get_text()[0]
                        file.write(ad_title)
                        file.write('\r\n')
                    ad_img = info.select("a.class#report-qboss > img")
                    print ad_img
                    if ad_img:
                        ad_img = re.findall(pattern=self.pattern, string=str(info))[0]
                        file.write(ad_img)
                        file.write('\r\n')
                    viewer = info.select("b.style")
                    print viewer
                    if viewer:
                        viewer = viewer.get_text()[0]
                        file.write(viewer)
                        file.write('\r\n')

    def crawl(self, root_url):
        driver = webdriver.Firefox(executable_path=r'D:\fireFoxDrive\geckodriver.exe')
        driver.set_page_load_timeout(50)
        driver.get(root_url)
        driver.implicitly_wait(10)
        # driver.find_element_by_id('login_div')
        # if u"QQ空间-分享生活，留住感动" in driver.title:
        self.login(driver=driver)
        # else:
        #     print "Crawl Failed."
        #     return None

    def login(self, driver):
        driver.switch_to.frame('login_frame')
        login_type = driver.find_element_by_id("switcher_plogin")
        login_type.click()
        time.sleep(3)
        user_name = driver.find_element_by_id("u")
        user_password = driver.find_element_by_id("p")
        login_button = driver.find_element_by_id("login_button")
        user_name.clear()
        user_name.send_keys(self.user)
        user_password.clear()
        user_password.send_keys(self.password)
        login_button.click()
        self.get_AD_info(driver)


if __name__ == '__main__':
    user = "xxxx"
    password = "xxxx"
    url = "https://user.qzone.qq.com/{}".format(user)
    qzone_spider = QzoneSpider(user=user, password=password)
    qzone_spider.crawl(root_url=url)

