# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from URLDownloader import myDownloader
from myRedis import MyRedis


class HTMLParser(object):
    def __init__(self, db, additional):
        self.d = myDownloader()
        self.redis = MyRedis(db, additional)

    def parser_url(self, city, url):
        web_data = self.d.downloader(url=url)
        if web_data:
            soup = BeautifulSoup(markup=web_data, features="lxml")

            car_urls = soup.find_all(name="a", attrs={"class": "aimg"})
            for car_url in car_urls:

                car_info_dict = {
                    "city": city,
                    "car_url": "https:" + str(car_url.attrs["href"])
                }
                print car_info_dict
                self.redis.save_urls(car_info_dict=car_info_dict)

            next_pages = soup.find_all(name="a", attrs={"name": "view_i"})
            if next_pages:
                next_page = next_pages[-1].text
                if next_page == u'下一页':
                    page_url = "https://www.xin.com" + str(next_pages[-1].attrs["href"])
                    print page_url
                    self.parser_url(city=city, url=page_url)

    def start_parser(self):
        city_dict = {
            "beijing": "https://www.xin.com/beijing/sn_t1000/",
            "shanghai": "https://www.xin.com/shanghai/sn_t1000/",
            "guangzhou": "https://www.xin.com/guangzhou/sn_t1000/",
            "shenzhen": "https://www.xin.com/shenzhen/sn_t1000/"
        }

        for city in city_dict:
            self.parser_url(city=city, url=city_dict[city])
