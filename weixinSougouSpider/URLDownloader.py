# -*- coding: utf-8 -*-

import time
import random
import requests
from weixinSougouSpider.userAgent import user_agent

headers = {
'Host': 'weixin.sogou.com',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:52.0) Gecko/20100101 Firefox/52.0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
'Accept-Encoding': 'gzip, deflate',
'Referer': 'http://weixin.sogou.com/antispider/?from=%2fweixin%3Ftype%3d1%26s_from%3dinput%26query%3dchinaunicom-nanqu',
'Cookie': 'ABTEST=0|1510479538|v1; IPLOC=CN5101; SUID=2DE3CF654A42910A000000005A0816B2; SUID=CB56AE753020910A000000005A0816B2; weixinIndexVisited=1; SUV=002D1751DF55DAD05A0816B6A47F6748; sct=8; SUIR=1510479545; SNUID=D845BD6713164ED97EDE21C21307EECB; JSESSIONID=aaatr1c0Rqv_r4LZxAv8v; PHPSESSID=2nr54vdatb8d7dhol86otir1a5; seccodeErrorCount=1|Sun, 12 Nov 2017 16:17:39 GMT; seccodeRight=success; successCount=1|Sun, 12 Nov 2017 16:17:48 GMT; refresh=1',
'Connection': 'keep-alive',
'Upgrade-Insecure-Requests': '1'
}


def downloader(url):
    time.sleep(20)
    print url
    s = requests.Session()
    web_data = s.get(url=url, headers=headers)
    # web_data = s.get(url=url, allow_redirects=False)
    # web_data = s.get(url=url)

    if web_data.status_code == 200:
        print "Requests ", url, web_data
        time.sleep(random.randint(1, 3))
        return web_data.text
    elif web_data.status_code == 302:
        print web_data.headers["Location"]
