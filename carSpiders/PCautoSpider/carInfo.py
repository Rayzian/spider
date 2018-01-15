# -*- coding: utf-8 -*-

import json
import traceback
import codecs
import re
from bs4 import BeautifulSoup
from URLDownloader import Downer
from DataOut import writeCarInfo, writeDelaer

import sys
reload(sys)
sys.setdefaultencoding('utf8')

class CarParser(object):

    def __init__(self):
        self.download = Downer()

    def car_info(self, car_info_dict):
        value_dict = eval(car_info_dict)

        web_data = self.download.downloader(url=value_dict["car_url"])
        if web_data:
            soup = BeautifulSoup(markup=web_data, features="lxml")

            title = soup.find(name="div", attrs={"class": "pos-mark"})
            if title:
                try:
                    title_split = title.text.strip().split(">")
                    car_brand = title_split[3].strip()
                    car_name = " ".join([i.strip() for i in title_split[4:6]])
                    # print "%s %s" % (car_brand, car_name)

                    car_id = re.compile(r'/m(\d+)?/').findall(string=value_dict["car_url"])[0]
                    # print car_id

                    price_div = soup.find(name="i", attrs={"id": "gfPrice_%s" % car_id})
                    if price_div:
                        price = price_div.text + u"万"
                        # print price

                    oil_div = soup.find(name="div", attrs={"class": "oil"})
                    electric_div = soup.find(name="div", attrs={"class": "electric"})

                    if oil_div:
                        engine = oil_div.contents[1].contents[3].contents[3].contents[1].contents[1]
                        # print engine
                    if electric_div:
                        engine = electric_div.contents[1].contents[3].contents[3].contents[3].contents[1]
                        # print engine

                    data = {
                        u"平台": u"太平洋汽车网",
                        u"车系": car_name,
                        u"价格": price,
                        u"品牌": car_brand,
                        u"汽车类型": value_dict["car_type"],
                        u"排量": engine,
                        u"车系编号": car_id,
                        "url": value_dict["car_url"]
                    }

                    writeCarInfo(data=data)
                    self.dealer_info(car_data=data)
                except Exception as e:
                    print traceback.format_exc(e)
                    with codecs.open(filename="detail_fail.txt", mode="a", encoding="utf-8") as f:
                        f.write((json.dumps(value_dict, ensure_ascii=False)))
                        f.write("\n")


    def dealer_info(self, car_data):

        city_dict = {
            "beijing": "http://price.pcauto.com.cn/dealer/interface/auto7/model/pocket_dealer_model_json.jsp?mid={car_id}&rid=2&pageNo=1&pageSize=999",
            "shanghai": "http://price.pcauto.com.cn/dealer/interface/auto7/model/pocket_dealer_model_json.jsp?mid={car_id}&pid=7&pageNo=1&pageSize=999",
            "guangzhou": "http://price.pcauto.com.cn/dealer/interface/auto7/model/pocket_dealer_model_json.jsp?mid={car_id}&rid=1&pageNo=1&pageSize=999",
            "shenzhen": "http://price.pcauto.com.cn/dealer/interface/auto7/model/pocket_dealer_model_json.jsp?mid={car_id}&rid=4&pageNo=1&pageSize=999"
        }

        for city in city_dict.keys():
            url = city_dict[city].format(car_id=car_data[u"车系编号"])
            dealer_data = self.download.downloader(url=url)

            if dealer_data:
                dealer_json = json.loads(s=dealer_data)
                for dealer in dealer_json[u'pay4sAndFreeDealers'][u'rows']:
                    dealer_name = "[%s]%s" % (dealer[u'aq'], dealer[u'shortName'])
                    dealer_data = {
                        "car_id": car_data[u"车系编号"],
                        "brand": car_data[u"车系"],
                        "name": dealer_name,
                        "phoneNumber": dealer[u'phone'],
                        "local": dealer[u'address']
                    }

                    writeDelaer(city=city, data=dealer_data)
