# -*- coding: utf-8 -*-

import codecs
import time
import requests
import traceback
import random
from userAgent import user_agent, proxy

count = 0


def downloader(url):
    global count
    if count > 3:
        with codecs.open(filename="failedUrl.txt", mode="a", encoding="utf-8") as fail:
            fail.write(url)
            fail.write("\n")

        print "Failed requests ", url
        count = 0
        return None

    try:
        headers = {
            'Host': 'www.chekb.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'https://www.baidu.com/link?url=8gXQT8Yvb0xzEF8DiNHUxgWLzQwKkWv1ehLelHERI4W&wd=&eqid=d208d81f00002b5e000000035a4aeaa3',
            'Cookie': 'gzl_msid=XvUPKb; Hm_lvt_9be185cce9ba8e43f8fcec302f165705=1513580086,1514859177; tma=65266044.24387019.1508918944161.1514859179308.1514949504165.3; tmd=85.65266044.24387019.1508918944161.; fingerprint=d807e682133522af19f27f56a511e0a0; bfd_g=88b502420a014e11000009080000526759f046a1; bdshare_firstime=1508919687162; Hm_lvt_2537bf315b3ced58dc45185602beea6d=1508920167,1508920236; gzl_cityid=8690; gzl_cityname=%E7%BB%B5%E9%98%B3; gzl_citycname=mianyang; Hm_lpvt_9be185cce9ba8e43f8fcec302f165705=1514949579; tmc=1.65266044.79666317.1514949579392.1514949579392.1514949579392',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'If-Modified-Since': 'Tue, 02 Jan 2018 02:00:15 GMT',
            'If-None-Match': '"c82f20-6861f-561c175bb19dc"',
            'Cache-Control': 'max-age=0'
        }
        session = requests.Session()
        time.sleep(0.5)
        web_data = session.get(url=url, headers=headers)
        if web_data.status_code == 200:
            print "Requests ", url, web_data
            if web_data.encoding == "ISO-8859-1":
                try:
                    return web_data.text.encode(web_data.encoding).decode(web_data.apparent_encoding)
                except Exception as e:
                    return web_data.text.encode('ISO-8859-1').decode("GB18030")
            return web_data.text
        else:
            print "Requests ", url, web_data

    except Exception as e:
        print traceback.format_exc(e)
        time.sleep(2)
        downloader(url=url)
        count += 1
