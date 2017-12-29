# -*- coding: utf-8 -*-

import json
from getJSON import downloader
from dataOut import writeData

count_index = 1

class Parser(object):
    def get_app_rank(self, rank_name):
        global count_index
        last_name = ""

        rank_info = {
            u"单机榜": [
                'http://main.appstore.vivo.com.cn/port/packages_top/?apps_per_page=20&elapsedtime=110571812&screensize=1440_2560&density=4.0&pictype=webp&cs=0&req_id=7&av=22&u=1101003132384733320065a660732300&an=5.1.1&app_version=1011&imei=861406037757645&nt=WIFI&id=2&page_index=1&cfrom=4&type=9&model=vivo+Xplay5A&s=2%7C290031484',
                'http://main.appstore.vivo.com.cn/port/packages_top/?apps_per_page=20&elapsedtime=110664894&screensize=1440_2560&density=4.0&pictype=webp&cs=0&req_id=7&av=22&u=1101003132384733320065a660732300&an=5.1.1&app_version=1011&imei=861406037757645&nt=WIFI&id=2&page_index=2&cfrom=4&type=9&model=vivo+Xplay5A&s=2%7C762841734',
                'http://main.appstore.vivo.com.cn/port/packages_top/?apps_per_page=20&elapsedtime=110696367&screensize=1440_2560&density=4.0&pictype=webp&cs=0&req_id=7&av=22&u=1101003132384733320065a660732300&an=5.1.1&app_version=1011&imei=861406037757645&nt=WIFI&id=2&page_index=3&cfrom=4&type=9&model=vivo+Xplay5A&s=2%7C2625042525',
                'http://main.appstore.vivo.com.cn/port/packages_top/?apps_per_page=20&elapsedtime=110758205&screensize=1440_2560&density=4.0&pictype=webp&cs=0&req_id=7&av=22&u=1101003132384733320065a660732300&an=5.1.1&app_version=1011&imei=861406037757645&nt=WIFI&id=2&page_index=4&cfrom=4&type=9&model=vivo+Xplay5A&s=2%7C2112159207',
                'http://main.appstore.vivo.com.cn/port/packages_top/?apps_per_page=20&elapsedtime=110785479&screensize=1440_2560&density=4.0&pictype=webp&cs=0&req_id=7&av=22&u=1101003132384733320065a660732300&an=5.1.1&app_version=1011&imei=861406037757645&nt=WIFI&id=2&page_index=5&cfrom=4&type=9&model=vivo+Xplay5A&s=2%7C1364339892',
                'http://main.appstore.vivo.com.cn/port/packages_top/?apps_per_page=20&elapsedtime=110817229&screensize=1440_2560&density=4.0&pictype=webp&cs=0&req_id=7&av=22&u=1101003132384733320065a660732300&an=5.1.1&app_version=1011&imei=861406037757645&nt=WIFI&id=2&page_index=6&cfrom=4&type=9&model=vivo+Xplay5A&s=2%7C4028996710',
                'http://main.appstore.vivo.com.cn/port/packages_top/?apps_per_page=20&elapsedtime=110837898&screensize=1440_2560&density=4.0&pictype=webp&cs=0&req_id=7&av=22&u=1101003132384733320065a660732300&an=5.1.1&app_version=1011&imei=861406037757645&nt=WIFI&id=2&page_index=7&cfrom=4&type=9&model=vivo+Xplay5A&s=2%7C489912450',
                'http://main.appstore.vivo.com.cn/port/packages_top/?apps_per_page=20&elapsedtime=110856946&screensize=1440_2560&density=4.0&pictype=webp&cs=0&req_id=7&av=22&u=1101003132384733320065a660732300&an=5.1.1&app_version=1011&imei=861406037757645&nt=WIFI&id=2&page_index=8&cfrom=4&type=9&model=vivo+Xplay5A&s=2%7C3300507189',
                'http://main.appstore.vivo.com.cn/port/packages_top/?apps_per_page=20&elapsedtime=110878745&screensize=1440_2560&density=4.0&pictype=webp&cs=0&req_id=7&av=22&u=1101003132384733320065a660732300&an=5.1.1&app_version=1011&imei=861406037757645&nt=WIFI&id=2&page_index=9&cfrom=4&type=9&model=vivo+Xplay5A&s=2%7C1384419617',
                'http://main.appstore.vivo.com.cn/port/packages_top/?apps_per_page=20&elapsedtime=110896789&screensize=1440_2560&density=4.0&pictype=webp&cs=0&req_id=7&av=22&u=1101003132384733320065a660732300&an=5.1.1&app_version=1011&imei=861406037757645&nt=WIFI&id=2&page_index=10&cfrom=4&type=9&model=vivo+Xplay5A&s=2%7C2643215656'

            ],
            u"网游榜": [
                'http://main.appstore.vivo.com.cn/port/packages_top/?apps_per_page=20&elapsedtime=111040435&screensize=1440_2560&density=4.0&pictype=webp&cs=0&req_id=8&av=22&u=1101003132384733320065a660732300&an=5.1.1&app_version=1011&imei=861406037757645&nt=WIFI&id=2&page_index=1&cfrom=4&type=10&model=vivo+Xplay5A&s=2%7C545720199',
                'http://main.appstore.vivo.com.cn/port/packages_top/?apps_per_page=20&elapsedtime=111057418&screensize=1440_2560&density=4.0&pictype=webp&cs=0&req_id=8&av=22&u=1101003132384733320065a660732300&an=5.1.1&app_version=1011&imei=861406037757645&nt=WIFI&id=2&page_index=2&cfrom=4&type=10&model=vivo+Xplay5A&s=2%7C1208913410',
                'http://main.appstore.vivo.com.cn/port/packages_top/?apps_per_page=20&elapsedtime=111078364&screensize=1440_2560&density=4.0&pictype=webp&cs=0&req_id=8&av=22&u=1101003132384733320065a660732300&an=5.1.1&app_version=1011&imei=861406037757645&nt=WIFI&id=2&page_index=3&cfrom=4&type=10&model=vivo+Xplay5A&s=2%7C3656736425',
                'http://main.appstore.vivo.com.cn/port/packages_top/?apps_per_page=20&elapsedtime=111091121&screensize=1440_2560&density=4.0&pictype=webp&cs=0&req_id=8&av=22&u=1101003132384733320065a660732300&an=5.1.1&app_version=1011&imei=861406037757645&nt=WIFI&id=2&page_index=4&cfrom=4&type=10&model=vivo+Xplay5A&s=2%7C1095037426',
                'http://main.appstore.vivo.com.cn/port/packages_top/?apps_per_page=20&elapsedtime=111106460&screensize=1440_2560&density=4.0&pictype=webp&cs=0&req_id=8&av=22&u=1101003132384733320065a660732300&an=5.1.1&app_version=1011&imei=861406037757645&nt=WIFI&id=2&page_index=5&cfrom=4&type=10&model=vivo+Xplay5A&s=2%7C3386481446',
                'http://main.appstore.vivo.com.cn/port/packages_top/?apps_per_page=20&elapsedtime=111121113&screensize=1440_2560&density=4.0&pictype=webp&cs=0&req_id=8&av=22&u=1101003132384733320065a660732300&an=5.1.1&app_version=1011&imei=861406037757645&nt=WIFI&id=2&page_index=6&cfrom=4&type=10&model=vivo+Xplay5A&s=2%7C3395042650',
                'http://main.appstore.vivo.com.cn/port/packages_top/?apps_per_page=20&elapsedtime=111137795&screensize=1440_2560&density=4.0&pictype=webp&cs=0&req_id=8&av=22&u=1101003132384733320065a660732300&an=5.1.1&app_version=1011&imei=861406037757645&nt=WIFI&id=2&page_index=7&cfrom=4&type=10&model=vivo+Xplay5A&s=2%7C255792302',
                'http://main.appstore.vivo.com.cn/port/packages_top/?apps_per_page=20&elapsedtime=111157233&screensize=1440_2560&density=4.0&pictype=webp&cs=0&req_id=8&av=22&u=1101003132384733320065a660732300&an=5.1.1&app_version=1011&imei=861406037757645&nt=WIFI&id=2&page_index=8&cfrom=4&type=10&model=vivo+Xplay5A&s=2%7C3156636719',
                'http://main.appstore.vivo.com.cn/port/packages_top/?apps_per_page=20&elapsedtime=111170743&screensize=1440_2560&density=4.0&pictype=webp&cs=0&req_id=8&av=22&u=1101003132384733320065a660732300&an=5.1.1&app_version=1011&imei=861406037757645&nt=WIFI&id=2&page_index=9&cfrom=4&type=10&model=vivo+Xplay5A&s=2%7C2422457197',
                'http://main.appstore.vivo.com.cn/port/packages_top/?apps_per_page=20&elapsedtime=111185087&screensize=1440_2560&density=4.0&pictype=webp&cs=0&req_id=8&av=22&u=1101003132384733320065a660732300&an=5.1.1&app_version=1011&imei=861406037757645&nt=WIFI&id=2&page_index=10&cfrom=4&type=10&model=vivo+Xplay5A&s=2%7C1727759399'
            ]
        }

        for app_url in rank_info[rank_name]:
            if (rank_name != last_name) and last_name:
                count_index = 1
            web_data = downloader(app_url, headers="main")
            if web_data:
                app_info_dict = json.loads(web_data)
                print app_info_dict
                for app_info in app_info_dict["value"]:
                    app_id = app_info["id"]
                    self.get_app_detail_info(app_id=app_id, count_index=count_index, rank_name=rank_name)
                    count_index += 1
            last_name = rank_name

    def get_app_detail_info(self, app_id, count_index, rank_name):
        url_template = ""
        if rank_name == u"单机榜":
            url_template = "http://info.appstore.vivo.com.cn/port/package/?elapsedtime=110937819&content_complete=1&screensize=1440_2560&ct=1&density=4.0&pictype=webp&cs=0&av=22&u=1101003132384733320065a660732300&an=5.1.1&app_version=1011&imei=861406037757645&nt=WIFI&module_id=11&id={app_id}&target=local&cfrom=11&need_comment=0&model=vivo+Xplay5A"
        elif rank_name == u"网游榜":
            url_template = "http://info.appstore.vivo.com.cn/port/package/?elapsedtime=111249007&content_complete=1&screensize=1440_2560&ct=1&density=4.0&pictype=webp&cs=0&av=22&u=1101003132384733320065a660732300&an=5.1.1&app_version=1011&imei=861406037757645&nt=WIFI&module_id=12&id={app_id}&target=local&cfrom=11&need_comment=0&model=vivo+Xplay5A"

        url = url_template.format(app_id=app_id)

        json_data = downloader(url=url, headers="info")

        if json_data:
            detail_app_info = json.loads(json_data)
            tag = " ".join([tag["tag"] for tag in detail_app_info["value"]["tags"]]) if "tags" in detail_app_info["value"] else " "
            app_data = {
                "rank": count_index,
                "name": detail_app_info["value"]["title_zh"] if detail_app_info["value"]["title_zh"] else
                detail_app_info["value"]["title_en"],
                "tag": tag,
                "introduction": " ".join(detail_app_info["value"]["introduction"].strip().split("\r")),
                "developer": detail_app_info["value"]["developer"]
            }
            print app_data

            writeData(data=app_data, rank_name=rank_name)
