# -*- coding: utf-8 -*-

import codecs
import time
import traceback
from bs4 import BeautifulSoup
from selenium import webdriver
from dataOut import writeData
from myRedis import MyRedis

import sys

reload(sys)
sys.setdefaultencoding('utf8')


class MySimuCrawl(object):
    def __init__(self, name, password):
        self.user = name
        self.password = password

    def crawl(self, root_url, company):
        driver = webdriver.Chrome(executable_path=r'D:\ChromeGeckoDriver\chromedriver.exe')
        driver.set_page_load_timeout(50)
        driver.get(root_url)
        driver.implicitly_wait(10)
        self.login(driver=driver)
        url = self.get_company_url(company=unicode(company.strip()), driver=driver)
        try:
            self.parser_company(driver=driver, company_url=url, company=company.strip())
        except Exception as e:
            with codecs.open(filename="failCompany_Conn.txt", mode="a", encoding="utf-8") as cf:
                cf.write("%s\n" % company.strip())
            driver.close()
            return
        driver.close()

    def login(self, driver):
        login_type = driver.find_element_by_xpath(
            ".//*[@id='web-content']/div/div/div/div[2]/div/div[2]/div[2]/div[1]/div[1]")
        login_type.click()
        time.sleep(1)

        user_name = driver.find_element_by_xpath(
            ".//*[@id='web-content']/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/input")
        password = driver.find_element_by_xpath(
            ".//*[@id='web-content']/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div[3]/input")
        login_button = driver.find_element_by_xpath(
            ".//*[@id='web-content']/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div[5]")
        user_name.clear()
        user_name.send_keys(self.user)
        time.sleep(1)
        password.clear()
        password.send_keys(self.password)
        time.sleep(1)
        login_button.click()
        time.sleep(5)

    def get_company_url(self, company, driver):
        if driver.find_element_by_id("home-main-search"):
            company_search = driver.find_element_by_xpath(".//*[@id='home-main-search']")
            button = driver.find_element_by_xpath(
                ".//*[@id='web-content']/div/div[1]/div[2]/div/div[2]/div[2]/div/div[1]/div[1]/div")
            company_search.clear()
            company_search.send_keys(company)
            time.sleep(1)
            button.click()
            time.sleep(5)

        elif driver.find_element_by_id("header-company-search"):
            company_search = driver.find_element_by_xpath(".//*[@id='header-company-search']")
            button = driver.find_element_by_xpath(".//*[@id='web-header']/div/div/div[1]/div[2]/div[2]/div[1]/div")
            company_search.clear()
            company_search.send_keys(company)
            time.sleep(1)
            button.click()
            time.sleep(5)

        web_data = driver.page_source
        soup = BeautifulSoup(markup=web_data, features="lxml")

        company_div = soup.find(name="a", attrs={"class": "query_name sv-search-company f18 in-block vertical-middle"})
        if company_div:
            company_url = company_div.attrs["href"]
            print company_url
            return company_url
        else:
            return None

    def parser_company(self, driver, company_url, company):
        info_dict = {}
        driver.get(company_url)
        driver.set_page_load_timeout(50)
        driver.implicitly_wait(10)

        contents = driver.page_source
        soup = BeautifulSoup(markup=contents, features="lxml")

        company_name = soup.find(name="span", attrs={"class": "f18 in-block vertival-middle sec-c2"})
        if company_name:
            info_dict["company_name"] = company_name.text

        legal_person = soup.find(name="div", attrs={"class": "f18 overflow-width sec-c3"})
        if legal_person:
            info_dict["legal_person"] = legal_person.text

        company_info = soup.find(name="div", attrs={"class": "base0910"})
        if company_info:
            info_dict["organizing_code"] = company_info.contents[0].contents[0].contents[0].contents[3].text
            info_dict["credit_code"] = company_info.contents[0].contents[0].contents[1].contents[1].text

        main_person = soup.find_all(name="div", attrs={"class": "staffinfo-module-container"})
        if main_person:
            info_dict["person_count"] = len(main_person)
            info_dict["position"] = [position.contents[0].contents[0].text.replace(",", " ") for position in main_person]
            info_dict["person"] = [person.contents[0].contents[1].text for person in main_person]

        stockholders = soup.find(name="div", attrs={"id": "_container_holder"})
        if stockholders:
            stockholder_list = stockholders.contents[0].contents[0].contents[1].contents
            info_dict["holder"] = [stockholder.contents[0].contents[0].text for stockholder in stockholder_list]
            info_dict["holder_prop"] = [stockholder.contents[1].text for stockholder in stockholder_list]

        try:
            writeData(info_dict)
            driver.close()
        except Exception as e:
            with codecs.open(filename="failCompany.txt", mode="a", encoding="utf-8") as cf:
                cf.write("%s\n" % company)
            driver.close()


if __name__ == '__main__':
    user = "x"
    password = "x"
    simu = MySimuCrawl(name=user, password=password)
    r = MyRedis(db="tianyancha", additional=True)

    if not r.check_urls_number():
        with open(name="D:\GitHubProject\spider\TianyanchaSpider\channel_cp_name.txt", mode="r") as ff:
            for temp in ff:
                r.save_urls(temp.strip())

    while (r.check_urls_number()):
        company = r.get_urls()
        url = "https://www.tianyancha.com/login"
        try:
            simu.crawl(root_url=url, company=company[0])
        except Exception as e:
            pass
        print "sleep 5S"
        time.sleep(5)
