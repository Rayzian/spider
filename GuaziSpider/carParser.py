# -*- coding: utf-8 -*-

import codecs
import json
import re
import threading
import traceback
from URLDownloader import downloader
from bs4 import BeautifulSoup

lock = threading.Lock()

def car_info(car_info_dict):
    # lock = threading.Lock()

    car_info_dict = eval(car_info_dict)
    web_data = downloader(url=car_info_dict["car_url"])

    if web_data:
        try:
            lock.acquire()
            soup = BeautifulSoup(markup=web_data, features="lxml")
            car = soup.find(name="h2", attrs={"class": "titlebox"}).next.strip()
            price = soup.find(name="span", attrs={"class": "pricestype"}).next[1:].strip()
            tables = soup.find(name="div", attrs={"class": "detailcontent clearfix js-detailcontent active"})
            brand = tables.contents[1].contents[3].contents[1].text
            print brand
            car_type = tables.contents[1].contents[4].contents[1].text
            print car_type
            enegin = tables.contents[1].contents[5].contents[1].text.split()[0]
            print enegin

            pattren = car_info_dict["city_re"] + "(\S+)?\.htm"
            data = {
                u"车系": car,
                u"价格": price + u"万",
                u"品牌": brand,
                u"汽车类型": car_type,
                u"排量": enegin,
                u"车系编号": re.compile(pattren).findall(string=car_info_dict["car_url"])[0],
                "url": car_info_dict["car_url"]
            }

            file_name = car_info_dict["city"] + "_carInfo"

            with codecs.open(filename=file_name, mode="a", encoding="utf-8") as cf:
                cf.write(json.dumps(data, ensure_ascii=False))
                cf.write("\n")

            lock.release()
        except Exception as e:
            lock.release()
            # print traceback.format_exc(e)
            # lock.release()
    # lock.release()