# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
from URLDownloader import downloader
from myRedis import MyRedis


class URLParser(object):
    def __init__(self, db, addtional=True):
        self.db = db
        self.redis = MyRedis(db=db, additional=addtional)

    def start_parser(self):
        car_type_url_dict = {
            "微型车": "http://car.qichedaquan.com/carConditionSelect/index?l=2&page=%s",
            "小型车": "http://car.qichedaquan.com/carConditionSelect/index?l=3&page=%s",
            "紧凑型车": "http://car.qichedaquan.com/carConditionSelect/index?l=4&page=%s",
            "中型车": "http://car.qichedaquan.com/carConditionSelect/index?l=5&page=%s",
            "中大型车": "http://car.qichedaquan.com/carConditionSelect/index?l=6&page=%s",
            "豪华车": "http://car.qichedaquan.com/carConditionSelect/index?l=7&page=%s",
            "小型SUV": "http://car.qichedaquan.com/carConditionSelect/index?l=10&page=%s",
            "紧凑型SUV": "http://car.qichedaquan.com/carConditionSelect/index?l=11&page=%s",
            "中型SUV": "http://car.qichedaquan.com/carConditionSelect/index?l=12&page=%s",
            "中大型SUV": "http://car.qichedaquan.com/carConditionSelect/index?l=13&page=%s",
            "大型SUV": "http://car.qichedaquan.com/carConditionSelect/index?l=14&page=%s",
            "跑车": "http://car.qichedaquan.com/carConditionSelect/index?l=15&page=%s",
            "面包车": "http://car.qichedaquan.com/carConditionSelect/index?l=16&page=%s",
            "皮卡": "http://car.qichedaquan.com/carConditionSelect/index?l=17&page=%s",
            "客车": "http://car.qichedaquan.com/carConditionSelect/index?l=18&page=%s"
        }

        for type_url in car_type_url_dict.keys():
            self.parser_url(car_type=type_url, url=car_type_url_dict[type_url])

    def parser_url(self, car_type, url):
        page = 1
        while True:
            serial_url = url % page
            web_data = downloader(url=serial_url)
            if web_data:
                soup = BeautifulSoup(markup=web_data, features="lxml")

                if not soup.find(name="div", attrs={"class": "str_bp"}):
                    break

                car_type_list = soup.find(name="ul", attrs={"class": "cart_type clearfix"})
                if car_type_list:
                    for car in car_type_list.contents:
                        if car != "\n":
                            serial_id = car.contents[5].attrs["data-id"]
                            urlspell = car.contents[5].attrs["data-urlspell"].strip()
                            for car_id in car.contents[5].attrs["data-ids"].split(","):
                                car_id = car_id.strip()
                                car_url = "http://car.qichedaquan.com/carparam/%s-%s?urlspell=%s" % (
                                    urlspell, car_id, urlspell)
                                serial_url_dict = {
                                    "serial_id": serial_id,
                                    "car_url": car_url,
                                    "car_type": car_type
                                }
                                print serial_url_dict
                                self.redis.save_urls(car_info_dict=serial_url_dict)
            page += 1
