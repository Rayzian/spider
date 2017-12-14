# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
from URLDownloader import downloader
from myRedis import MyRedis


class HTMLParser(object):

    def __init__(self, db):
        self.db = db
        self.redis = MyRedis(db=self.db, additional=True)


    def get_brand_url(self, url):
        web_data = downloader(url=url)
        soup = BeautifulSoup(markup=web_data, features="lxml")
        car_n_type = soup.find(name="div", attrs={"class": "marcenter"})
        for car_url_n_type in car_n_type:
            car_type = car_url_n_type.contents[1].contents
            if len(car_type) == 2:
                car_type = car_type[0]
            elif len(car_type) > 2:
                car_type = car_type[1]
            for cars in car_url_n_type.contents[3].contents[1].contents[1:-2]:
                for car in cars.contents[1:]:
                    brand_url = car.next.contents[1].contents[0].attrs["href"]
                    brand_dict = {
                        "car_type": car_type,
                        "brand_url": str(brand_url) + "?pliv=2.0"
                    }

                    self.get_car_url(brand_dict=brand_dict)


    def get_car_url(self, brand_dict):
        web_data = downloader(brand_dict["brand_url"])
        soup = BeautifulSoup(markup=web_data, features="lxml")
        p_divs = soup.find_all(name="p", attrs={"class": "p1"})
        for p_div in p_divs:
            url = p_div.contents[0].attrs["href"]
            car_dict = {
                "car_type": brand_dict["car_type"],
                "car_url": url
            }
            self.redis.save_urls(car_info_dict=car_dict)

