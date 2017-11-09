# -*- coding: utf-8 -*-

import json
from AppSpiders.pcsuite360.URLDownloader import downloader
from AppSpiders.pcsuite360.DataOut import writeData


class Paser(object):
    def json_parse(self, url, plat, type):
        web_data = downloader(url=url)
        if web_data:
            vaule = json.loads(web_data)

            count = 1
            for data in vaule["data"]:
                if type == "new_games":
                    self.__new_game_parse(data, count, plat, type)
                    count += 1
                elif type == "good_sales":
                    self.__good_sales_parse(data, count, plat, type)
                    count += 1

    def __new_game_parse(self, data, count, plat, type):

        detail_url = "http://openbox.mobilem.360.cn/Iservice/AppDetail?s_stream_app=1" \
                     "&market_id=360market&sort=1" \
                     "&pname={}" \
                     "&isAd=0&prepage=game_ranking_%E6%96%B0%E6%A6%9C_%E5%85%A8%E9%83%A8" \
                     "&curpage=appinfo&os=19&os_version=4.4.4&vc=300070109&v=7.1.9" \
                     "&md=MuMu&sn=6.119186756728438&cpu=&ca1=x86" \
                     "&ca2=armeabi-v7a&m=94a9af57156152abdd51228b0a31c7a6" \
                     "&m2=a6b2959a7e642787f4d28fd04dc2b942&ch=110149" \
                     "&ppi=720_1280&startCount=1&pvc=82&pvn=1.0.82&re=1&tid=0&cpc=1&snt=-1&nt=1&" \
                     "gender=-1&age=0&theme=2&br=Android&s_3pk=1".format(data["apkid"])

        detail_web_data = downloader(url=detail_url)

        if detail_web_data:
            detail_value = json.loads(detail_web_data)
            detail_dict = detail_value["data"][0]

            data = {
                u"排名": count,
                u"游戏名称": detail_dict["name"],
                u"题材": detail_dict["tag"],
                u"游戏介绍": detail_dict["brief"],
                u"标签": detail_dict["list_tag"],
                u"开发商": detail_dict["corp"]
            }

            writeData(data=data, plat=plat, type=type)

    def __good_sales_parse(self, data, count, plat, type):
        detail_url = "http://openbox.mobilem.360.cn/Iservice/AppDetail?s_stream_app=1" \
                     "&market_id=360market&sort=1" \
                     "&pname={}" \
                     "&isAd=0&prepage=game_ranking_%E7%83%AD%E6%A6%9C_%E5%85%A8%E9%83%A8" \
                     "&curpage=appinfo&os=19&os_version=4.4.4&vc=300070109&v=7.1.9" \
                     "&md=MuMu&sn=6.119186756728438&cpu=&ca1=x86&ca2=armeabi-v7a" \
                     "&m=94a9af57156152abdd51228b0a31c7a6&m2=a6b2959a7e642787f4d28fd04dc2b942&" \
                     "ch=110149&ppi=720_1280&startCount=1&pvc=82" \
                     "&pvn=1.0.82&re=1&tid=0&cpc=1&snt=-1&nt=1&gender=-1" \
                     "&age=0&theme=2&br=Android&s_3pk=1".format(data["apkid"])

        detail_web_data = downloader(url=detail_url)

        if detail_web_data:
            detail_value = json.loads(detail_web_data)
            detail_dict = detail_value["data"][0]

            data = {
                u"排名": count,
                u"游戏名称": detail_dict["name"],
                u"题材": detail_dict["tag"],
                u"游戏介绍": detail_dict["brief"],
                u"标签": detail_dict["list_tag"],
                u"开发商": detail_dict["corp"]
            }

            writeData(data=data, plat=plat, type=type)