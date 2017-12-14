# -*- coding: utf-8 -*-

import codecs
import json
import re
import threading
import traceback
from URLDownloader import myDownloader
from bs4 import BeautifulSoup

lock = threading.Lock()

def car_info(car_info_dict):
    # lock = threading.Lock()
    d = myDownloader()

    car_info_dict = eval(car_info_dict)
    web_data = d.downloader(url=car_info_dict)
    lock.acquire()
    if web_data:
        try:
            soup = BeautifulSoup(markup=web_data, features="lxml")
            # print web_data
            car = soup.find(name="span", attrs={"class": "cd_m_h_tit"}).text.strip()
            price = soup.find(name="span", attrs={"class": "cd_m_info_jg"}).text.strip()[1:]
            enegin = soup.find_all(name="span", attrs={"class": "cd_m_desc_val"})[-2].text
            brand = soup.find(name="div", attrs={"class": "cd_m_i_pz"}).contents[3].contents[3]
            # print type(brand)
            car_brand = brand.text.strip().split(" ")[-1]
            # print "brand:", brand.contents[3].contents[3].text.strip().split(" ")[-1]
            car_type = soup.find(name="div", attrs={"class": "cd_m_i_pz"}).contents[3].contents[5].text.strip().split(" ")[-1]
            # car_type = str(car_type)
            data = {
                u"车系": car,
                u"价格": price,
                u"品牌": car_brand,
                u"汽车类型": car_type,
                u"排量": enegin,
                u"车系编号": re.compile(r'/che(\d+).?').findall(string=car_info_dict["car_url"])[0],
                "url": car_info_dict["car_url"],
                u"平台": u"优信二手车网"
            }

            file_name = car_info_dict["city"] + "_carInfo"

            with codecs.open(filename=file_name, mode="a", encoding="utf-8") as cf:
                cf.write(json.dumps(data, ensure_ascii=False))
                cf.write("\n")

            lock.release()
        except Exception as e:
            print traceback.format_exc(e)
            print car_info_dict
            with codecs.open(filename="failedUrl.txt", mode="a", encoding="utf-8") as fail:
                fail.write(json.dumps(car_info_dict, ensure_ascii=False))
                fail.write("\n")
            lock.release()
    else:
        lock.release()