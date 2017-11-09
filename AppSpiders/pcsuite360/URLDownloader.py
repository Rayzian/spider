# -*- coding: utf-8 -*-

import random
import requests
import time


def downloader(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; U; Android 4.4.4; zh-cn; MuMu Build/V417IR) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30;360appstore"
    }

    s = requests.Session()

    web_data = s.get(url=url, headers=headers)

    if web_data.status_code == 200:
        print "Requests ", url, web_data.status_code
        time.sleep(random.randint(1, 3))
        return web_data.text
    return None
