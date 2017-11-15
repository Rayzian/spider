# -*- coding: utf-8 -*-

import codecs
import time
import requests
import traceback
import random
from userAgent import user_agent, proxy

count = 0


def downloader(url, headers=None):
    global count
    if count > 3:
        with codecs.open(filename="failedUrl.txt", mode="a", encoding="utf-8") as fail:
            fail.write(url)
            fail.write("\n")

        print "Failed requests ", url
        return None

    try:
        if not headers:
            headers = {
                "User_Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:56.0) Gecko/20100101 Firefox/56.0"
            }
        else:
            headers = headers
        # proxies = proxy()
        session = requests.Session()
        time.sleep(2)
        # web_data = session.get(url=url, headers=headers, proxies=proxies)
        web_data = session.get(url=url, headers=headers)
        if web_data.status_code == 200:
            print "Requests ", url, web_data
            return web_data.text
        else:
            print url, web_data

    except Exception as e:
        print traceback.format_exc(e)
        time.sleep(3)
        downloader(url=url)
        count += 1
