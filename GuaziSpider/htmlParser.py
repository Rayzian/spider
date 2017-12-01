# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
from URLDownloader import downloader
from myRedis import MyRedis


class HTMLParser(object):
    def __init__(self, db, additional):
        self.redis = MyRedis(db, additional)

    def parser_url(self, city, url):
        web_data = downloader(url=url)
        if web_data:
            soup = BeautifulSoup(markup=web_data, features="lxml")

            cars = soup.find_all(name="a", attrs={"class": "car-a"})
            if cars:
                for car in cars:
                    car_url = "https://www.guazi.com" + car.attrs["href"]
                    print car_url

                    car_info_dict = {
                        "city": city,
                        "car_url": car_url,
                        "city_re": re.compile(r'com(\S+)?buy').findall(string=url)[0]
                    }
                    print car_info_dict
                    self.redis.save_urls(car_info_dict=car_info_dict)

                next_page = soup.find(name="a", attrs={"class": "next"})
                if next_page:
                    page = next_page.attrs["href"]
                    next_url = "https://www.guazi.com" + page
                    self.parser_url(city=city, url=next_url)



    def start_parser(self):
        city_dict = {
            "beijing": "https://www.guazi.com/bj/buy/",
            "shanghai": "https://www.guazi.com/sh/buy/",
            "guangzhou": "https://www.guazi.com/gz/buy/",
            "shenzhen": "https://www.guazi.com/sz/buy/"
        }

        for city in city_dict:
            self.parser_url(city=city, url=city_dict[city])