# -*- coding: utf-8 -*-

import json
import re
from URLDownloader import downloader
from myRedis import MyRedis




class HTMLParser(object):
    def __init__(self, db, additional):
        self.pattern_api = re.compile(r'jsonpCallback(.*)')
        self.redis = MyRedis(db=db, additional=additional)

    def _downloader(self, url):
        web_data = downloader(url=url)

        if web_data:
            match_results = self.pattern_api.findall(web_data)[0]

            result_dict = eval(match_results)

            return result_dict

    def parse(self):
        url_temp = "http://select.car.yiche.com/selectcartool/searchresult?l={l}&page={page}&external=Car&v=20171011&callback=jsonpCallback"
        url_list = []
        car_type_url_dict = {
            u"微型": "http://select.car.yiche.com/selectcartool/searchresult?l=1&external=Car&v=20171011&callback=jsonpCallback",
            u"小型": "http://select.car.yiche.com/selectcartool/searchresult?l=2&external=Car&v=20171011&callback=jsonpCallback",
            u"紧凑型": "http://select.car.yiche.com/selectcartool/searchresult?l=3&external=Car&v=20171011&callback=jsonpCallback",
            u"中型": "http://select.car.yiche.com/selectcartool/searchresult?l=5&external=Car&v=20171011&callback=jsonpCallback",
            u"中大型": "http://select.car.yiche.com/selectcartool/searchresult?l=4&external=Car&v=20171011&callback=jsonpCallback",
            u"豪华型": "http://select.car.yiche.com/selectcartool/searchresult?l=6&external=Car&v=20171011&callback=jsonpCallback",
            u"MPV": "http://select.car.yiche.com/selectcartool/searchresult?l=7&external=Car&v=20171011&callback=jsonpCallback",
            u"小型SUV": "http://select.car.yiche.com/selectcartool/searchresult?l=13&external=Car&v=20171011&callback=jsonpCallback",
            u"紧凑型SUV": "http://select.car.yiche.com/selectcartool/searchresult?l=14&external=Car&v=20171011&callback=jsonpCallback",
            u"中型SUV": "http://select.car.yiche.com/selectcartool/searchresult?l=15&external=Car&v=20171011&callback=jsonpCallback",
            u"中大型SUV": "http://select.car.yiche.com/selectcartool/searchresult?l=16&external=Car&v=20171011&callback=jsonpCallback",
            u"全尺寸SUV": "http://select.car.yiche.com/selectcartool/searchresult?l=17&external=Car&v=20171011&callback=jsonpCallback",
            u"跑车": "http://select.car.yiche.com/selectcartool/searchresult?l=9&external=Car&v=20171011&callback=jsonpCallback",
            u"面包车": "http://select.car.yiche.com/selectcartool/searchresult?l=11&external=Car&v=20171011&callback=jsonpCallback",
            u"皮卡": "http://select.car.yiche.com/selectcartool/searchresult?l=12&external=Car&v=20171011&callback=jsonpCallback",
            u"客车": "http://select.car.yiche.com/selectcartool/searchresult?l=18&external=Car&v=20171011&callback=jsonpCallback",
        }
        for car_type in car_type_url_dict.keys():

            l = re.compile(r'\?l=(\d+)?&').findall(string=car_type_url_dict[car_type])[0]

            result_dict = self._downloader(url=car_type_url_dict[car_type])

            if int(result_dict["Count"]) / 20 == 2 or int(result_dict["Count"]) / 20 == 1:
                url_list.append(url_temp.format(l=l, page="2"))
            elif int(result_dict["Count"]) / 20 > 2:
                [url_list.append(url_temp.format(l=l, page=(i + 2))) for i in range(int(result_dict["Count"]) / 20)]

            self._save_data(result_dict=result_dict, car_type=car_type)

            for new_url in url_list:
                print "get new_url", new_url
                new_result_dict = self._downloader(url=new_url)
                self._save_data(result_dict=new_result_dict, car_type=car_type)

            url_list = []

    def _save_data(self, result_dict, car_type):
        for result in result_dict["ResList"]:

            car_id_list = result["CarIdList"].strip().split(",")[: -1]
            for car_id in car_id_list:
                data = {
                    "car_id": car_id,
                    "car_type": car_type,
                    "url": "http://car.bitauto.com/%s/m%s/" % (result["AllSpell"], car_id)
                }

                self.redis.save_urls(data)
