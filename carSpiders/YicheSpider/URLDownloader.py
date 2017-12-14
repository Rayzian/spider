# -*- coding: utf-8 -*-

import traceback
import codecs
import requests
import time
from userAgent import user_agent

# count = 0

def downloader(url, headers=None):
    get_url = ""
    # global count
    # if count > 3:
    #     with codecs.open(filename="failedUrl.txt", mode="a", encoding="utf-8") as fail:
    #         fail.write(str(url))
    #         fail.write("\n")
    #
    #     print "Failed requests ", url
    #     count = 0
    #     return None

    try:
        if not headers:
            headers = headers
        else:
            headers = {
                "User-Agent": user_agent()
            }
        # proxies = proxy()
        session = requests.Session()
        time.sleep(1)
        # web_data = session.get(url=url, headers=headers, proxies=proxies)
        if isinstance(url, dict):
            get_url = url["url"]
        elif isinstance(url, str):
            get_url = url
        web_data = session.get(url=get_url, headers=headers)
        if web_data.status_code == 200:
            try:
                print "Requests ", get_url, web_data
                return web_data.text
            except:
                return web_data
        else:
            print get_url, web_data

    except Exception as e:
        print traceback.format_exc(e)
        with codecs.open(filename="failedUrl.txt", mode="a", encoding="utf-8") as fail:
            fail.write(str(url))
            fail.write("\n")
        # count += 1