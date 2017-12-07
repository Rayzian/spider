# -*- coding: utf-8 -*-

import time
import redis
from bs4 import BeautifulSoup
from selenium import webdriver


class MySimuCrawl(object):
    def __init__(self, name, password):
        self.user = name
        self.password = password
        self.redis = redis.Redis(host="localhost", port=6379, db="tianyancha")

    def login(self, driver):
        # driver.switch_to.frame("_input input_nor contactphone")
        login_type = driver.find_element_by_xpath(
            ".//*[@id='web-content']/div/div/div/div[2]/div/div[2]/div[2]/div[1]/div[1]")
        login_type.click()
        time.sleep(3)

        user_name = driver.find_element_by_xpath(
            ".//*[@id='web-content']/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/input")
        password = driver.find_element_by_xpath(
            ".//*[@id='web-content']/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div[3]/input")
        login_button = driver.find_element_by_xpath(
            ".//*[@id='web-content']/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div[5]")
        user_name.clear()
        user_name.send_keys(self.user)
        time.sleep(3)
        password.clear()
        password.send_keys(self.password)
        time.sleep(3)
        login_button.click()
        time.sleep(10)

    def crawl(self, root_url):
        driver = webdriver.Chrome(executable_path=r'D:\ChromeGeckoDriver\chromedriver.exe')
        driver.set_page_load_timeout(50)
        driver.get(root_url)
        driver.implicitly_wait(10)
        self.login(driver=driver)
        self.get_company_url(company="腾讯科技", driver=driver)

    def get_company_url(self, company, driver):
        if driver.find_element_by_id("home-main-search"):
            company_search = driver.find_element_by_xpath(".//*[@id='home-main-search']")
            button = driver.find_element_by_xpath(
                ".//*[@id='web-content']/div/div[1]/div[2]/div/div[2]/div[2]/div/div[1]/div[1]/div")
            company_search.clear()
            company_search.send_keys(unicode(company))
            time.sleep(3)
            button.click()
            time.sleep(10)

        elif driver.find_element_by_id("header-company-search"):
            company_search = driver.find_element_by_xpath(".//*[@id='header-company-search']")
            button = driver.find_element_by_xpath(".//*[@id='web-header']/div/div/div[1]/div[2]/div[2]/div[1]/div")
            company_search.clear()
            company_search.send_keys(company)
            time.sleep(3)
            button.click()
            time.sleep(10)

        web_data = driver.page_source
        soup = BeautifulSoup(markup=web_data, features="lxml")

        company_div = soup.find(name="a", attrs={"class": "query_name sv-search-company f18 in-block vertical-middle"})
        if company_div:
            company_url = company_div["attrs"]
            print company_url
            return company_url


    def parser_company(self, driver, company_url):
        info_dict = {}
        driver.get(company_url)
        driver.set_page_load_timeout(50)

        contents = driver.page_source
        soup = BeautifulSoup(markup=contents, features="lxml")

        company_name = soup.find(name="span", attrs={"class": "f18 in-block vertival-middle sec-c2"})
        if company_name:
            info_dict["company_name"] = company_name.text

        legal_person = soup.find(name="div", attrs={"class": "f18 overflow-width sec-c3"})
        if legal_person:
            info_dict["legal_person"] = legal_person.contents[1].text

if __name__ == '__main__':
    user = "17381540262"
    password = "password11415269"
    simu = MySimuCrawl(name=user, password=password)

    url = "https://www.tianyancha.com/login"
    simu.crawl(root_url=url)
