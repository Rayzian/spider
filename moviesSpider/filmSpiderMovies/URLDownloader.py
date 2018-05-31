# -*- coding: utf-8 -*-

import time
import requests


class Download(object):
    def downloader(self, url):

        time.sleep(3)

        s = requests.Session()
        web_data = s.get(url=url)

        if web_data.status_code == 200:
            return web_data.text
        else:
            return False
