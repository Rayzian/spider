# -*- coding: utf-8 -*-

import Queue
import re
from bs4 import BeautifulSoup
from XcarSpider.URLDownloader import downloader
from XcarSpider.myRedis import MyRedis


class HTMLParser(object):
    def __init__(self, db):
        self.db = db
        self.redis = MyRedis(db, additional=True)
        self.start_q = Queue.Queue()
        self.car_urls = Queue.Queue()
        self.pattern1 = re.compile(r'<a href="/(\d+)/?"')
        self.pattern2 = re.compile(r'<a href="(/m\d+?/)"')

    def _parser_car_series(self):
        url = "http://newcar.xcar.com.cn/price/"
        web_data = downloader(url=url)

        car_series_list = self.pattern1.findall(string=web_data)

        if car_series_list:
            for car_series in car_series_list:
                car_url = "http://newcar.xcar.com.cn/%s/" % str(car_series)
                self.start_q.put(car_url)
                self.start_q.task_done()


    def get_car_detail_url(self):
        self._parser_car_series()
        car_info_dict = {}
        if not self.start_q.empty():
            while (not self.start_q.empty()):
                task_url = self.start_q.get(timeout=1)
                web_data = downloader(task_url)
                if web_data:
                    soup = BeautifulSoup(markup=web_data, features="lxml")
                    car_info_dict["car_brand"] = soup.find(name="span", attrs={"class": "lt_f1"}).text[:-1]
                    table_bord_list = soup.find_all(name="tr", attrs={"class": "table_bord"})
                    if table_bord_list:
                        for table_bord in table_bord_list:
                            index = self.pattern2.findall(str(table_bord))
                            if index:
                                car_info_dict["car_url"] = "http://newcar.xcar.com.cn" + str(index[0])

            # print "Put car_url into redis."
                                self.redis.save_urls(car_info_dict)

            print "Put all urls done."
        else:
            print "Cannot get car`s url"
            raise