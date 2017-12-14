# -*- coding: utf-8 -*-

import traceback
import re
import threading
from bs4 import BeautifulSoup
from URLDownloader import downloader
from DataOut import writeDelaer, writeCarInfo

lock = threading.Lock()

class CarInfoParser(object):
    def car_info_parse(self, car_dict):
        # lock.acquire()
        car_info_dict = eval(car_dict)
        web_data = downloader(car_info_dict["car_url"])
        if web_data:
            try:
                brand = None
                serise = None
                engine = None
                price = None
                soup = BeautifulSoup(markup=web_data, features="lxml")
                ul = soup.find(name="ul", attrs={"class": "crumbs_list"})
                div = soup.find(name="div", attrs={"class": "crumbs l"})
                if ul:
                    brand = ul.contents[5].text[:-2].strip()
                    serise = unicode(ul.contents[7].contents[1]).strip()[1:]

                    price = soup.find(name="span", attrs={"class": "cxk-jg2"}).text if soup.find(name="span", attrs={
                        "class": "cxk-jg2"}) else None
                    engine = re.compile(r'<span >(\d\.\dL)</span>').findall(string=web_data)[0] if re.compile(
                        r'<span >(\d\.\dL)</span>').findall(string=web_data) else None

                elif div:
                    brand = div.contents[6].text
                    serise = div.contents[8].contents[2].text
                    price = soup.find_all(name="p", attrs={"class": "clearfix"})[1].contents[1].text
                    engine = soup.find(name="ul", attrs={"class": "canshu_list"}).contents[7].contents[2].text
                    if not engine:
                        engine = None
                car_id = re.compile(r'/index(\d+)?.shtml').findall(string=car_info_dict["car_url"])
                if serise and brand:
                    data = {
                        u"平台": u"58车",
                        "url": car_info_dict["car_url"],
                        u"车系编号": car_id[0],
                        u"车系": serise,
                        u"汽车类型": car_info_dict["car_type"],
                        u"品牌": brand,
                        u"排量": engine,
                        u"价格": price
                    }

                    writeCarInfo(data=data)
                    self.delear_info_parse(data=data)
                # lock.release()
            except Exception as e:
                print traceback.format_exc(e)
                # lock.release()


    def delear_info_parse(self, data):
        # lock.acquire()
        city_dict = {
            "beijing": "http://product.58che.com/index.php?c=Ajax_ProPage&a=GetDealer&pid=1&cid=0&id={car_id}&ap={count}&page=1",
            "shanghai": "http://product.58che.com/index.php?c=Ajax_ProPage&a=GetDealer&pid=2&cid=0&id={car_id}&ap={count}&page=1",
            "guangzhou": "http://product.58che.com/index.php?c=Ajax_ProPage&a=GetDealer&pid=30&cid=347&id={car_id}&ap={count}&page=1",
            "shenzhen": "http://product.58che.com/index.php?c=Ajax_ProPage&a=GetDealer&pid=30&cid=348&id={car_id}&ap={count}&page=1"
        }

        for city in city_dict.keys():
            for count in [1, 2]:
                url = city_dict[city].format(car_id=data[u"车系编号"], count=count)
                web_data = downloader(url=url)
                if web_data:
                    soup = BeautifulSoup(markup=web_data, features="lxml")
                    lis = soup.find_all(name="div", attrs={"class": "namebox"})
                    if lis:
                        for li in lis[:-1]:
                            delear_data = {
                                "car_id": data[u"车系编号"],
                                "brand": data[u"车系"],
                                "name": li.contents[1].text,
                                "phoneNumber": li.contents[3].contents[3].text.strip(),
                                "address": li.contents[5].text.strip()[3:]
                            }

                            writeDelaer(data=delear_data, city=city)
        # lock.release()

