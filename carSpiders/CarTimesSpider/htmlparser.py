# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
from myRedis import MyRedis
from URLDownloader import downloader

import sys

reload(sys)
sys.setdefaultencoding('utf8')


class HTMLParser(object):
    def __init__(self, db):
        self.db = db
        self.redis = MyRedis(db=db, additional=True)

    def html_parser(self, url):
        web_data = downloader(url=url)
        if web_data:
            brand_list = eval(web_data)
            for brand in brand_list:
                brand_url = "http://car.autotimes.com.cn/price/ab%s/" % brand["id"].strip()
                print "brand_url: ", brand_url
                car_web_data = downloader(url=brand_url)
                if car_web_data:
                    car_url = "http://car.autotimes.com.cn/price%s"
                    soup = BeautifulSoup(markup=car_web_data, features="lxml")
                    serises_list = soup.find_all(name="div", attrs={"class": "quop_pplb_1 quop_pplb_12"})[:-1]
                    for serises in serises_list:
                        serises_id = serises.contents[3].contents[0].contents[1].contents[0].attrs["href"][2:]
                        serises_url = car_url % serises_id
                        print "serises_url: ", serises_url
                        serises_web_data = downloader(url=serises_url)
                        if serises_web_data:
                            soup = BeautifulSoup(markup=serises_web_data, features="lxml")
                            car_div = soup.find(name="div", attrs={"class": "quop_pplb_4"})
                            detail_url = car_div.contents[0].attrs["href"]
                            print "detail_url: ", detail_url
                            detail_web_data = downloader(url=detail_url)
                            if detail_web_data:
                                soup = BeautifulSoup(markup=detail_web_data, features="lxml")
                                dealer = soup.find(name="div", attrs={"class": "n_gtop_39"})
                                if dealer:
                                    serises_id = \
                                        re.compile(r'/price/(\S+)?/').findall(string=dealer.contents[0].attrs["href"])[
                                            0]
                                    print "serises_id: ", serises_id

                                    detail_url = detail_url + "config/"

                                    serises_dict = {
                                        "detail_url": detail_url,
                                        "serises_id": serises_id
                                    }

                                    self.redis.save_urls(serises_dict)
