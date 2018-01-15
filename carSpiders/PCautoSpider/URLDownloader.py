# -*- coding: utf-8 -*-

import codecs
import time
import requests
import traceback
import random
from userAgent import user_agent, proxy

class Downer(object):

    def __init__(self):
        self.count = 0

    def downloader(self, url, headers=None):
        if self.count > 2:
            with codecs.open(filename="failedUrl.txt", mode="a", encoding="utf-8") as fail:
                fail.write(url)
                fail.write("\n")

            print "Failed requests ", url
            self.count = 0
            return None

        try:
            if not headers:
                headers = {
                    "User_Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:52.0) Gecko/20100101 Firefox/52.0"
                }
            else:
                headers = headers
            session = requests.Session()
            time.sleep(1)
            web_data = session.get(url=url, headers=headers)
            if web_data.status_code == 200:
                print "Requests ", url, web_data
                return web_data.text
            else:
                print url, web_data

        except Exception as e:
            print traceback.format_exc(e)
            time.sleep(3)
            self.downloader(url=url)
            self.count += 1
