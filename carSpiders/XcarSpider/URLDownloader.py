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
            "User_Agent": user_agent()
        }
        session = requests.Session()
        # time.sleep(0.5)
        web_data = session.get(url=url, headers=headers)
        if web_data.status_code == 200:
            print "Requests ", url, web_data
            if web_data.encoding == "ISO-8859-1":
                try:
                    return web_data.text.encode(web_data.encoding).decode(web_data.apparent_encoding)
                # except Exception as e:
                #     return web_data.text.encode('ISO-8859-1').decode('UTF-8')
                except Exception as e:
                    return web_data.text.encode('ISO-8859-1').decode("GB18030")
            return web_data.text

    except Exception as e:
        print traceback.format_exc(e)
        time.sleep(2)
        downloader(url=url)
        count += 1
