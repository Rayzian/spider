# -*- coding: utf-8 -*-

import traceback
import re
from URLDownloader import downloader
from bs4 import BeautifulSoup
from DataOut import writeDelaer, writeCarInfo

import sys
reload(sys)
sys.setdefaultencoding('utf8')

class InfoParser(object):

    def car_info(self, info_dict):
        engine = ""
        car_info_dict = eval(info_dict)
        web_data = downloader(url=car_info_dict["car_url"])

        if web_data:
            soup = BeautifulSoup(markup=web_data, features="lxml")
            title = soup.find(name="p", attrs={"class": "imgs_c_crumbs"})
            title_split = title.text.strip().split(">")
            brand = title_split[2].strip()
            print "brand: ", brand
            serises = " ".join(title_split[3:]).strip()
            print "serises: ", serises

            engine_div = soup.find(name="div", attrs={"class": "car_msg_price"})
            if engine_div:
                if car_info_dict["car_type"] != '新能源':
                    engine = re.compile(r'(\d+\.\d+\w)').findall(string=engine_div.contents[1].contents[1].text)[
                        0] if re.compile(r'(\d+\.\d+\w)').findall(
                        string=engine_div.contents[1].contents[1].text) else None
                if car_info_dict["car_type"] == '新能源':
                    engine = re.compile(r'(\d+)').findall(string=engine_div.contents[1].contents[3].text)[
                                 0] + "KW" if re.compile(r'(\d+)').findall(
                        string=engine_div.contents[1].contents[3].text) else None
            car_id = re.compile(r'-(\d+)\?urlspell').findall(string=car_info_dict["car_url"])

            price = soup.find(name="span", attrs={"class": "fright font14"}).contents[1].text if soup.find(name="span",
                                                                                                           attrs={
                                                                                                               "class": "fright font14"}) else None

            data = {
                u"平台": u"汽车大全",
                "url": car_info_dict["car_url"],
                u"车系编号": car_id[0],
                u"车系": serises,
                u"汽车类型": car_info_dict["car_type"],
                u"品牌": brand,
                u"排量": engine,
                u"价格": price
            }

            writeCarInfo(data=data)
            self.dealer_info_parser(data=data, car_info_dict=car_info_dict)

    def dealer_info_parser(self, data, car_info_dict):

        dealer_url = "http://car.qichedaquan.com/dealer/queryList?cityId={city_id}&locationId=0&serialId={serial_id}&carId={car_id}&modelId=0&pageSize=100&pageNo=1&orderType=0"

        city_dict = {
            "beijing": "201",
            "shanghai": "2401",
            "guangzhou": "501",
            "shenzhen": "502"
        }

        for city in city_dict.keys():
            url = dealer_url.format(city_id=city_dict[city], serial_id=car_info_dict["serial_id"], car_id=data[u"车系编号"])

            web_data = downloader(url=url)
            if web_data:
                dealer_list = eval(web_data)
                for dealer in dealer_list["dataList"]:
                    try:
                        name = "[{modelName}]{shortName}".format(modelName=dealer["modelName"], shortName=dealer["shortName"])
                        dealer_data = {
                            "name": name,
                            "phoneNumber": dealer["servicePhone"],
                            "address": dealer["address"],
                            "car_id": data[u"车系编号"],
                            "brand": data[u"车系"]
                        }

                        writeDelaer(data=dealer_data, city=city)
                    except Exception as e:
                        pass

