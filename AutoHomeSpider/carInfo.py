# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
from URLDownloader import downloader
from DataOut import writeCarInfo, writeDelaer


class CarInfoParser(object):
    def infoParser(self, url, series_id, car_brand):
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
            try:
                engine = soup.find(name="div", attrs={"class": "cardetail-infor-car"}).contents[1].contents[12].contents[
                    1] if soup.find(name="div", attrs={"class": "cardetail-infor-car"}) else None
            except:
                engine = soup.find(name="div", attrs={"class": "cardetail-infor-car"}).contents[1].contents[13].contents[
                    1] if soup.find(name="div", attrs={"class": "cardetail-infor-car"}) else None

            data = {
                u"平台": u"汽车之家",
                u"品牌": car_brand,
                u"汽车类型": brand[0],
                u"价格": price,
                "url": url,
                u"车系编号": series_id,
                u"车系": " ".join(brand[1:]),
                u"排量": engine
            }
            writeCarInfo(data)
            return brand

    def dealerParses(self, series_id, car_id, brand):
        print "start to parse dealer"
        headers = {
            'Host': 'dealer.autohome.com.cn',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linu…) Gecko/20100101 Firefox/56.0',
            'Accept': 'text/html,application/xhtml+xm…plication/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'If-Modified-Since': 'Wed, 15 Nov 2017 10:23:56 GMT',
            'Cache-Control': 'max-age=0'
        }

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
                print "dealer url: ", detail_url

                data = downloader(url=detail_url, headers=headers)
                if data:

                    soup = BeautifulSoup(markup=data, features="lxml")
                    local = soup.find_all(name="dl", attrs={"class": "dl-list dl-one"})
                    if local:
                        for i in local:
                            data = {
                                "local": "".join(i.contents[7].text.split()),
                                "name": i.contents[1].text.strip(),
                                "phoneNumber": i.contents[5].text.strip(),
                                "car_id": car_id
                            }
                            writeDelaer(data=data, city=city, brand=brand)
                            index_count += 1
                    else:
                        index_count = 1
                        break
                else:
                    break

    def carParser(self, url):
        web_data = downloader(url=url)
        if web_data:
            series_id = re.compile(r'/(\d+)/').findall(string=url)[0]

            soup = BeautifulSoup(markup=web_data, features="lxml")
            car_brand = soup.find(name="div", attrs={"class": "subnav-title-name"})
            if car_brand:
                car_brand = car_brand.contents[1].next[:-1]
            car_spec_list = soup.find(name="div", attrs={"id": "speclist20"}).attrs["data-list"].split(",")

            for car_spec in car_spec_list:
                car_link = soup.find("p", attrs={"data-gcjid": car_spec}).parent.contents[1].contents[1].attrs["href"]
                web_url = "https://www.autohome.com.cn%s" % car_link
                brand = self.infoParser(url=web_url, series_id=car_spec, car_brand=car_brand)
                if brand:
                    self.dealerParses(series_id=series_id, car_id=car_spec, brand=brand)
