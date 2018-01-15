# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
from URLDownloader import downloader
from myRedis import MyRedis

class CarURLParse(object):

    def __init__(self, db, additional):
        self.redis = MyRedis(db, additional)

    def start_parser(self):
        city_dict = {
            "beijing": "https://www.renrenche.com/bj/ershouche/",
            "shanghai": "https://www.renrenche.com/sh/ershouche/",
            "guangzhou": "https://www.renrenche.com/gz/ershouche/",
            "shenzhen": "https://www.renrenche.com/sz/ershouche/"
        }

        for city in city_dict:
            self.parser_url(city=city, url=city_dict[city])

    def parser_url(self, city, url):
        web_data = downloader(url=url)
        soup = BeautifulSoup(markup=web_data, features="lxml")
        car_list = soup.find_all(name="li", attrs={"class": "span6 list-item car-item"})
        if car_list:
            for car in car_list:
                car_url = "https://www.renrenche.com" + str(car.contents[1].attrs["href"])

                car_dict = {
                    "city": city,
                    "car_url": car_url
                }

                self.redis.save_urls(car_info_dict=car_dict)

            next_page = soup.find(name="a", attrs={"rrc-event-name": "switchright"})
            if next_page:
                if next_page.attrs["href"] != "javascript:void(0);":
                    next_page_url = "https://www.renrenche.com" + str(next_page.attrs["href"])
                    print next_page_url
                    self.parser_url(city=city, url=next_page_url)