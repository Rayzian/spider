# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from URLDownloader import Downer
from myRedis import MyRedis


class htmlParser(object):
    def __init__(self, db):
        self.download = Downer()
        self.db = db
        self.redis = MyRedis(db=self.db, additional=True)

    def get_brand_url(self):

        car_dict = {
            "微型车": "http://price.pcauto.com.cn/cars/q-k76.html",
            "小型车": "http://price.pcauto.com.cn/cars/q-k110.html",
            "紧凑型车": "http://price.pcauto.com.cn/cars/q-k73.html",
            "中型车": "http://price.pcauto.com.cn/cars/q-k72.html",
            "中大型车": "http://price.pcauto.com.cn/cars/q-k71.html",
            "大型车": "http://price.pcauto.com.cn/cars/q-k70.html",
            "小型SUV": "http://price.pcauto.com.cn/cars/q-k131.html",
            "紧凑型SUV": "http://price.pcauto.com.cn/cars/q-k132.html",
            "中型SUV": "http://price.pcauto.com.cn/cars/q-k133.html",
            "中大型SUV": "http://price.pcauto.com.cn/cars/q-k134.html",
            "大型SUV": "http://price.pcauto.com.cn/cars/q-k135.html",
            "MPV": "http://price.pcauto.com.cn/cars/q-k74.html",
            "跑车": "http://price.pcauto.com.cn/cars/q-k111.html",
            "微面": "http://price.pcauto.com.cn/cars/q-k77.html",
            "微卡": "http://price.pcauto.com.cn/cars/q-k93.html",
            "轻客": "http://price.pcauto.com.cn/cars/q-k105.html",
            "皮卡": "http://price.pcauto.com.cn/cars/q-k94.html"
        }

        for car_key in car_dict.keys():
            car_type_brand_url = car_dict[car_key]
            car_type = car_key

            web_data = self.download.downloader(url=car_type_brand_url)
            if web_data:
                soup = BeautifulSoup(markup=web_data, features="lxml")
                serial_list = soup.find_all(name="p", attrs={"class": "tit"})
                if serial_list:
                    for serial in serial_list:
                        serial_url = "http://price.pcauto.com.cn" + serial.contents[1].attrs["href"]

                        self.save_car_url(car_type=car_type, serial_url=serial_url)

    def save_car_url(self, car_type, serial_url):
        web_data = self.download.downloader(url=serial_url)
        if web_data:
            soup = BeautifulSoup(markup=web_data, features="lxml")
            car_list = soup.find_all(name="p", attrs={"class": "name"})
            if car_list:
                for car in car_list:
                    try:
                        car_url = "http://price.pcauto.com.cn" + car.contents[1].attrs["href"]
                        print car_url

                        car_info_dict = {
                            "car_type": car_type,
                            "car_url": car_url
                        }
                        print car_info_dict

                        self.redis.save_urls(car_info_dict=car_info_dict)

                    except:
                        pass
