# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
from XcarSpider.URLDownloader import downloader
from XcarSpider.DataOut import writeDelaer, writeCarInfo


class CarInfo(object):
    def _car_info_parse(self, car_info_dict):
        info = eval(car_info_dict)
        car_id = re.compile(r'/m(\d+)?/').findall(string=info["car_url"])
        if car_id:
            car_id = car_id[0]

        web_data = downloader(info["car_url"])
        brand = []
        if web_data:
            soup = BeautifulSoup(markup=web_data, features="lxml")
            index = soup.find(name="div", attrs={"class": "place"})
            brand.extend(index.text.strip().split(">")[1: -1])
            ref_ul = soup.find(name="ul", attrs={"class": "ref_ul"})
            brand.extend(ref_ul.text.strip().split("\n"))
            price = unicode(soup.find(name="a", attrs={"onclick": "clicklog(124663);"}).text) + u'万' if soup.find(
                name="a", attrs={"onclick": "clicklog(124663);"}) else None

            data = {
                u"平台": u"爱卡汽车",
                "url": info["car_url"],
                u"车系编号": car_id,
                u"车系": " ".join(brand[1: 3]),
                u"汽车类型": brand[0],
                u"品牌": info["car_brand"],
                u"排量": brand[-1].split(":")[-1],
                u"价格": price
            }
            writeCarInfo(data=data)
            return data

    def _delaer_parse(self, car_id, brand):
        city_dict = {
            "beijing": "475",
            "shanghai": "507",
            "guangzhou": "347",
            "shenzhen": "348"
        }

        for city in city_dict.keys():
            url = "http://newcar.xcar.com.cn/auto/index.php?" \
                  "r=newcar/ModelIndex/GetDealerAjax&mid=%s&city_id=%s&iss=1&page=1&order=0" % (car_id, city_dict[city])

            web_data = downloader(url)
            if web_data:
                soup = BeautifulSoup(markup=web_data, features="lxml")
                delear_list = soup.find_all(name="div", attrs={"class": "sell"})
                if delear_list:
                    for delear in delear_list:
                        data = {
                            "name": " ".join(delear.text.strip().split()),
                            "phoneNumber": delear.parent.contents[3].text,
                            "address": delear.parent.contents[5].text,
                            "car_id": car_id
                        }

                        writeDelaer(data=data, city=city, brand=brand)

    def car_parse(self, car_info_dict):
        data = self._car_info_parse(car_info_dict=car_info_dict)
        self._delaer_parse(car_id=data[u"车系编号"], brand=data[u"车系"])
