# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from URLDownloader import downloader
from DataOut import writeCarInfo


class CarInfoParser(object):
    def car_parser(self, url):
        web_data = downloader(url=url)
        soup = BeautifulSoup(markup=web_data, features="lxml")
        detail_info = soup.find(name="div", attrs={"id": "car_con2"})
        price = detail_info.contents[1].contents[1].contents[1].contents[1].text.strip()
        serises = soup.find(name="div", attrs={"class": "allBorder page"}).text.strip().split(">")[-1].strip()
        engine = detail_info.contents[3].contents[3].contents[1].contents[1].text.strip()
        brand = detail_info.contents[1].contents[3].contents[1].contents[1].text.strip()
        car_type = detail_info.contents[1].contents[3].contents[3].contents[1].text.strip()
        car_id = url.strip().split("/")

        data = {
            u"平台": u"汽车大世界",
            "url": url,
            u"车系编号": car_id[-2],
            u"车系": serises,
            u"汽车类型": car_type,
            u"品牌": brand,
            u"排量": engine,
            u"价格": price
        }

        writeCarInfo(data=data)
