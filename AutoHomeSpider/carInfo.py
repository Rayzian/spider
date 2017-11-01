# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
from URLDownloader import downloader
from DataOut import writeCarInfo, writeDelaer


class CarInfoParser(object):
    def infoParser(self, url, series_id):
        print "start to parse car_info."
        data = downloader(url=url)
        if data:

            soup = BeautifulSoup(markup=data, features="lxml")
            tag = soup.find(name="div", attrs={"class": "breadnav fn-left"}) if soup.find(name="div", attrs={
                "class": "breadnav fn-left"}) else None
            brand = [index.strip() for index in tag.text.split(">")[1: -1]] if [index.strip() for index in
                                                                                tag.text.split(">")[1: -1]] else None
            price = soup.find(name="li", attrs={"class": "li-price fn-clear"}).contents[1].attrs["data-price"] if \
            soup.find(name="li", attrs={"class": "li-price fn-clear"}).contents[1].attrs["data-price"] else None

            data = {
                "brand": brand,
                "price": price,
                "url": url,
                "series_id": series_id
            }
            writeCarInfo(data)
            return brand

    def dealerParses(self, series_id, car_id, brand):
        print "start to parse dealer"

        # detail_url = "https://dealer.autohome.com.cn/frame/spec/32014/310000/310100/0/0/1/10?isPage=1&seriesId=3170&source=defalut&kindId=1&isPriceAuth=0"
        index_count = 1
        local_id_dict = {
            "beijing": "110000/110100",
            "shanghai": "310000/310100",
            "guangzhou": "440000/440100",
            "shenzhen": "440000/440300"
        }
        for city in local_id_dict.keys():
            print "city: ", city
            while True:
                detail_url = "https://dealer.autohome.com.cn/frame/spec" \
                             "/%s/%s/0/0/%s/10" \
                             "?isPage=1&seriesId=%s&source=defalut&kindId=1&isPriceAuth=0" % (
                                 car_id, local_id_dict[city], str(index_count), series_id)

                data = downloader(url=detail_url)
                if data:

                    soup = BeautifulSoup(markup=data, features="lxml")
                    local = soup.find_all(name="dl", attrs={"class": "dl-list dl-one"})
                    if local:
                        for i in local:
                            data = {
                                "local": "".join(i.contents[7].text.split()),
                                "name": i.contents[1].text.strip(),
                                "phoneNumber": i.contents[5].text.strip(),
                                "series_id": series_id,
                                "car_id": car_id
                            }
                            writeDelaer(data=data, city=city, brand=brand)
                            index_count += 1
                    else:
                        index_count = 1
                        break

    def carParser(self, url):
        web_data = downloader(url=url)
        if web_data:
            series_id = re.compile(r'/(\d+)/').findall(string=url)[0]

            soup = BeautifulSoup(markup=web_data, features="lxml")
            car_spec_list = soup.find(name="div", attrs={"id": "speclist20"}).attrs["data-list"].split(",")

            for car_spec in car_spec_list:
                car_link = soup.find("p", attrs={"data-gcjid": car_spec}).parent.contents[1].contents[1].attrs["href"]
                web_url = "https://www.autohome.com.cn%s" % car_link
                brand = self.infoParser(url=web_url, series_id=series_id)
                if brand:
                    self.dealerParses(series_id=series_id, car_id=car_spec, brand=brand)
