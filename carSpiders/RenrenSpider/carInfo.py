# -*- coding: utf-8 -*-

import json
import codecs
from bs4 import BeautifulSoup
from URLDownloader import downloader


def car_parser(car_info_dict):
    car_dict = eval(car_info_dict)
    web_data = downloader(url=car_dict["car_url"])

    if web_data:
        soup = BeautifulSoup(markup=web_data, features="lxml")
        title = soup.find(name="p", attrs={"class": "detail-breadcrumb-tagP"})
        if title:
            serial = title.text.strip().split(">")[-1].strip()
            # print serial

            price = soup.find(name="p", attrs={"class": "price detail-title-right-tagP"})
            if price:
                car_price = price.text.strip()[1:]
                # print car_price
            engine = soup.find(name="li", attrs={"class": "span displacement"})
            if engine:
                car_engine = engine.contents[1].contents[1].text.strip()
                # print car_engine
            base_params = soup.find(name="table", attrs={"id": "basic-parms"})
            if base_params:
                car_type = base_params.contents[3].contents[1].contents[3].text.strip()
                car_brand = base_params.contents[3].contents[5].contents[3].text.strip()
                # print car_type, car_brand

            car_id = car_dict["car_url"].strip().split("/")[-1].strip()
            # print car_id

            data = {
                u"车系": serial,
                u"价格": car_price,
                u"品牌": car_brand,
                u"汽车类型": car_type,
                u"排量": car_engine,
                u"车系编号": car_id,
                "url": car_dict["car_url"],
                u"平台": u"人人二手车"
            }

            file_name = car_dict["city"] + "_carInfo"

            with codecs.open(filename=file_name, mode="a", encoding="utf-8") as cf:
                cf.write(json.dumps(data, ensure_ascii=False))
                cf.write("\n")
