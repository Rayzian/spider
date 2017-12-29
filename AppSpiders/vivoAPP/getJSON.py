# -*- coding: utf-8 -*-

import requests
import time

def downloader(url, headers):

    print "sleep 10s"
    time.sleep(10)
    if headers == "main":
        headers = {
            'accept-encoding': 'gzip',
            'Host': 'main.appstore.vivo.com.cn',
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2) Gecko/20100115 Firefox/3.6'
        }
    elif headers == "info":
        headers = {
            'accept-encoding': 'gzip',
            'Host': 'info.appstore.vivo.com.cn',
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2) Gecko/20100115 Firefox/3.6'
        }

    s = requests.Session()
    web_data = s.get(url=url, headers=headers)

    if web_data.status_code == 200:
        print url, web_data.status_code
        return web_data.text
    else:
        print url, web_data