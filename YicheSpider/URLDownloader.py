# -*- coding: utf-8 -*-

import traceback
import codecs
import requests
import time
from userAgent import user_agent

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
            headers = headers
        else:
            headers = {
                "User-Agent": user_agent()
            }
        # proxies = proxy()
        session = requests.Session()
        time.sleep(2)
        # web_data = session.get(url=url, headers=headers, proxies=proxies)
        web_data = session.get(url=url, headers=headers)
        if web_data.status_code == 200:
            try:
                print "Requests ", url, web_data
                return web_data.text
            except:
                return web_data
        else:
            print url, web_data

    except Exception as e:
        print traceback.format_exc(e)
        time.sleep(3)
        downloader(url=url)
        count += 1