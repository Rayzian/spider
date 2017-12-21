# -*- coding: utf-8 -*-

import threading
import codecs
import time
import requests
import traceback
import random
from userAgent import user_agent, proxy

count = 0
lock = threading.Lock()


def downloader(url):
    # lock.acquire()
    global count
    if count > 3:
        with codecs.open(filename="failedUrl.txt", mode="a", encoding="utf-8") as fail:
            fail.write(url)
            fail.write("\n")
        count = 0

        print "Failed requests ", url
        # lock.release()
        return None

    try:
        headers = {
            "User_Agent": user_agent()
        }
        session = requests.Session()
        time.sleep(0.5)
        web_data = session.get(url=url, headers=headers)
        if web_data.status_code == 200:
            print "Requests ", url, web_data
            # lock.release()
            return web_data.text

    except Exception as e:
        print traceback.format_exc(e)
        time.sleep(2)
        downloader(url=url)
        count += 1
        # lock.release()
