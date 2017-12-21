# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from URLDownloader import downloader
from DataOut import writeCarInfo, writeDelaer

import sys

reload(sys)
sys.setdefaultencoding('utf8')


class carParser(object):
    def car_parse(self, serises_dict):
        value_dict = eval(serises_dict)
        web_data = downloader(url=value_dict["detail_url"])
        if web_data:
            car_info_list = []
            car_id_list = []
            soup = BeautifulSoup(markup=web_data, features="lxml")
            car_list = soup.find(name="table", attrs={"id": "autotop"})
            if car_list:
                for car in car_list.contents[1].contents[1:]:
                    if car != "\n":
                        car_id_list.append(car.attrs["name"])

                for car_id in car_id_list:
                    detail_info = soup.find_all(name="td", attrs={"name": car_id})
                    data = {
                        u"平台": u"汽车时代网",
                        u"车系": detail_info[0].text.strip().split("\n")[0].strip(),
                        u"价格": detail_info[1].text.strip(),
                        u"品牌": detail_info[3].text.strip(),
                        u"汽车类型": detail_info[4].text.strip(),
                        u"排量": "null" if detail_info[6].text == "" else detail_info[6].text,
                        u"车系编号": car_id,
                        "url": value_dict["detail_url"] + car_id + ".html"
                    }
                    car_info_list.append(data)
                if car_info_list:
                    writeCarInfo(data_list=car_info_list)
                    self.dealer_info(car_info_list=car_info_list, serises_dict=value_dict)

    def dealer_info(self, car_info_list, serises_dict):

        city_dict = {
            "beijing": "http://dealer.autotimes.com.cn/beijing/{serises_id}/?page={page}",
            "shanghai": "http://dealer.autotimes.com.cn/shanghai/{serises_id}/?page={page}",
            "guangzhou": "http://dealer.autotimes.com.cn/guangzhou/{serises_id}/?page={page}",
            "shenzhen": "http://dealer.autotimes.com.cn/shenzhen/{serises_id}/?page={page}"
        }

        for city in city_dict:
            page = 1
            serises_id = serises_dict["serises_id"]
            while True:
                url = city_dict[city].format(page=page, serises_id=serises_id)
                web_data = downloader(url=url)
                if web_data:
                    soup = BeautifulSoup(markup=web_data, features="lxml")
                    dealers_list = soup.find_all(name="div", attrs={"class": "shangjia_liebiao_le4"})
                    if dealers_list:
                        for car_info in car_info_list:
                            for dealer in dealers_list:
                                dealer_name = dealer.contents[1].text.strip()
                                dealer_telephone = dealer.contents[5].contents[0].contents[5].text.strip().split("：")[
                                    -1]
                                dealer_address = dealer.contents[5].contents[0].contents[3].attrs["title"].strip()
                                dealer_dict = {
                                    "car_id": car_info[u"车系编号"],
                                    "brand": car_info[u"车系"],
                                    "name": dealer_name,
                                    "phoneNumber": dealer_telephone,
                                    "address": dealer_address
                                }
                                if dealer_name and dealer_telephone and dealer_address:
                                    writeDelaer(data=dealer_dict, city=city)
                        page += 1
                    else:
                        break
                else:
                    break
