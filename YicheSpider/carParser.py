# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
from URLDownloader import downloader
from DataOut import writeCarInfo, writeDelaer


class Parser(object):
    def __init__(self):
        self.engine_pattern2 = re.compile(r'<span class="info">(\d+kw)?</span>')
        self.engine_pattern1 = re.compile(r'<span class="info">(\d+\.\dL)?</span>')

    def car_info_parser(self, car_dict):
        web_data = downloader(url=car_dict)

        if web_data:
            soup = BeautifulSoup(markup=web_data, features="lxml")

            tags = soup.find(name="div", attrs={"class": "crumbs-txt"}).text.strip().split(">")[-3:]
            price = soup.find(name="div", attrs={"class": "mid row"}).contents[1].text.strip().split("\n")[1]

            if self.engine_pattern1.findall(string=web_data):
                engine = self.engine_pattern1.findall(string=web_data)[0]
            elif self.engine_pattern2.findall(string=web_data):
                engine = self.engine_pattern2.findall(string=web_data)[0]
            else:
                engine = u"暂无"

            data = {
                u"平台": u"易车网",
                u"品牌": tags[0],
                u"汽车类型": car_dict["car_type"],
                u"价格": price,
                "url": car_dict["url"],
                u"车系编号": car_dict["car_id"],
                u"车系": "".join(tags[1:]),
                u"排量": engine
            }

            writeCarInfo(data=data)

            return tags


    def car_delaer_info(self, car_dict, tags):

        delaer_data = {}

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:52.0) Gecko/20100101 Firefox/52.0",
            "Host": "price.bitauto.com",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Connection": "keep-alive",
            "If-Modified-Since": "Tue, 21 Nov 2017 02:47:30 GMT",
            "Upgrade-Insecure-Requests": "1"
        }

        city_dict = {
            "beijing": "201",
            "shanghai": "2401",
            "guangzhou": "501",
            "shenzhen": "502"
        }

        for city in city_dict.keys():
            city_id = city_dict[city]

            url = "http://price.bitauto.com/nc%s_c%s/" % (car_dict["car_id"], city_id)

            web_data = downloader(url=url, headers=headers)
            if web_data:
                soup = BeautifulSoup(markup=web_data, features="lxml")

                delaer_list = soup.find_all(name="div", attrs={"class": "col-xs-6 left"})
                for delaer in delaer_list:
                    if len(delaer.contents) == 4:
                        delaer_data = {
                            "local": delaer.contents[2].text.strip().split(":")[-1],
                            "name": delaer.contents[0].contents[0].text,
                            "phoneNumber": delaer.contents[3].contents[1].next,
                            "car_id": car_dict["car_id"]
                        }
                    elif len(delaer.contents) == 3:
                        delaer_data = {
                            "local": delaer.contents[1].text.strip().split(":")[-1],
                            "name": delaer.contents[0].contents[0].text,
                            "phoneNumber": delaer.contents[2].contents[1].next,
                            "car_id": car_dict["car_id"]
                        }
                    writeDelaer(city=city, data=delaer_data, brand=tags)

    def car_parser(self, car_dict):
        car_info = eval(car_dict)
        tags = self.car_info_parser(car_dict=car_info)
        self.car_delaer_info(car_dict=car_info, tags=tags)
