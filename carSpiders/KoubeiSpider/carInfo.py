# -*- coding: utf-8 -*-

import re
import json
from URLDownloader import downloader
from bs4 import BeautifulSoup
from DataOut import writeDelaer, writeCarInfo


class CarParser(object):
    def car_info(self, car_info):
        car_info_dict = eval(car_info)
        web_data = downloader(url=car_info_dict["car_url"])
        if web_data:
            soup = BeautifulSoup(markup=web_data, features="lxml")
            title = soup.find(name="div", attrs={"class": "navigatev1New"})
            if title:
                serial_name = title.text.strip().split(">")[-1].strip()
            info_ul = soup.find(name="ul", attrs={"class": "info_ul"})
            if info_ul:
                price = info_ul.contents[3].contents[2].text.strip()
                brand = info_ul.contents[5].contents[1][1:].strip()
                engine = info_ul.contents[13].contents[1][1:].strip()
                car_type = info_ul.contents[21].contents[1][1:].strip()
            car_id = car_info_dict["car_url"].strip().split("/")[-2]

            data = {
                u"平台": u"汽车口碑网",
                "url": car_info_dict["car_url"],
                u"车系编号": car_id,
                u"车系": serial_name,
                u"汽车类型": car_type,
                u"品牌": brand,
                u"排量": engine,
                u"价格": price
            }

            writeCarInfo(data=data)
            self.dealer_parser(car_data=data, car_info_dict=car_info_dict)

    def dealer_parser(self, car_data, car_info_dict):

        dealer_city = {
            "beijing": "http://www.chekb.com/etools/setcityjs.php?action=cxingjxs&aid={car_id}&cityid=1296&cityname=%E5%8C%97%E4%BA%AC&cname=beijing&ccid1={ccid}",
            "guangzhou": "http://www.chekb.com/etools/setcityjs.php?action=cxingjxs&aid={car_id}&cityid=1304&cityname=%E5%B9%BF%E5%B7%9E&cname=guangzhou&ccid1={ccid}",
            "shanghai": "http://www.chekb.com/etools/setcityjs.php?action=cxingjxs&aid={car_id}&cityid=8203&cityname=%E4%B8%8A%E6%B5%B7&cname=shanghai&ccid1={ccid}"
        }

        for city in dealer_city.keys():
            city_url = dealer_city[city].format(car_id=car_data[u"车系编号"], ccid=car_info_dict[u"ccid"])
            print city_url
            web_data = downloader(url=city_url)
            if web_data:
                web_data_json = json.loads(s=web_data)
                soup = BeautifulSoup(markup=web_data_json["dealerBox"], features="lxml")
                dealer_info_list = soup.find_all(name="ul", attrs={"class": "dealerCx"})
                if dealer_info_list:
                    for dealer_info in dealer_info_list:
                        dealer_type = dealer_info.contents[0].contents[0].text.strip()
                        dealer_name = dealer_info.contents[0].contents[1].text.strip()
                        dealer_phone = dealer_info.contents[2].contents[1].text.strip()
                        dealer_address = dealer_info.contents[3].contents[1].attrs["href"].strip()

                        dealer_data = {
                            "car_id": car_data[u"车系编号"],
                            "brand": car_data[u"车系"],
                            "name": "%s%s" % (dealer_type, dealer_name),
                            "phoneNumber": dealer_phone,
                            "address": dealer_address
                        }
                        if dealer_name and dealer_phone and dealer_address:
                            writeDelaer(city=city, data=dealer_data)
