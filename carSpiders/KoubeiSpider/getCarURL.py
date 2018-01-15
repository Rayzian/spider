# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
from myRedis import MyRedis
from URLDownloader import downloader

class URLParser(object):

    def __init__(self, db, addtional=True):
        self.db = db
        self.redis = MyRedis(db=db, additional=addtional)

    def start_parser(self):
        carType_url_list = [
            "http://www.chekb.com/weixingche/brand.html",
            "http://www.chekb.com/xiaoxingche/brand.html",
            "http://www.chekb.com/jincouxingche/brand.html",
            "http://www.chekb.com/zhongxingche/brand.html",
            "http://www.chekb.com/zhongdaxingche/brand.html",
            "http://www.chekb.com/haohuache/brand.html",
            "http://www.chekb.com/suv/brand.html",
            "http://www.chekb.com/mpv/brand.html",
            "http://www.chekb.com/paoche/brand.html",
            "http://www.chekb.com/pika/brand.html",
            "http://www.chekb.com/mianbaoche/brand.html"
        ]

        for carType_url in carType_url_list:
            web_data = downloader(url=carType_url)
            if web_data:
                soup = BeautifulSoup(markup=web_data, features="lxml")
                serials = soup.find_all(name="a", attrs={"class": "co1e"})
                if serials:
                    for serial in serials:
                        serial_url = serial.attrs["href"]
                        print serial_url

                        car_web_data = downloader(url=serial_url)
                        if car_web_data:
                            soup = BeautifulSoup(markup=car_web_data, features="lxml")
                            ccid = re.compile(r'ccid1=(\w+)').findall(string=car_web_data)
                            if ccid:
                                print ccid[0]
                            cars = soup.find_all(name="td", attrs={"class": "left"})
                            if cars:
                                for car in cars:
                                    car_url = car.contents[0].attrs["href"]
                                    # title = unicode(car.contents[0].attrs["title"])
                                    car_url_dict = {
                                        "ccid": ccid[0],
                                        "car_url": car_url
                                    }
                                    self.redis.save_urls(car_info_dict=car_url_dict)