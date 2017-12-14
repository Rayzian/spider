# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from URLDownloader import downloader
from myRedis import MyRedis

class HTMLParser(object):

    def __init__(self, db):
        self.db = db
        self.redis = MyRedis(db=self.db, additional=True)


    def get_brand_url(self, url):
        web_data = downloader(url=url)
        if web_data:
            soup = BeautifulSoup(markup=web_data, features="lxml")
            brands = soup.find_all(name="div", attrs={"class": "car_py_con"})
            for brand in brands:
                for brand_detail in brand.contents[3].contents[:-2]:
                    if brand_detail != "\n":
                        brand_url = brand_detail.contents[1].attrs["href"]
                        self.get_car_url(url=brand_url)

    def get_car_url(self, url):
        web_data = downloader(url=url)
        if web_data:
            soup = BeautifulSoup(markup=web_data, features="lxml")
            car_contents = soup.find_all(name="span", attrs={"class": "sp1"})
            for car_content in car_contents:
                car_url = car_content.contents[0].next.attrs["href"]
                self.save_car_url(url=car_url)

    def save_car_url(self, url):
        web_data = downloader(url=url)
        if web_data:
            soup = BeautifulSoup(markup=web_data, features="lxml")
            cars = soup.find_all(name="td", attrs={"class": "cc1"})
            for car in cars[:-1]:
                self.redis.save_urls(car.next.attrs["href"])