# -*- coding: utf-8 -*-

import time
import random
import requests
import traceback

count = 0


def downloader(url):
    global count
    assert count < 3
    try:
        session = requests.Session()
        web_data = session.get(url=url)
        if web_data.status_code == 200:
            time.sleep(random.randint(1, 4))
            return web_data.text

    except Exception as e:
        print traceback.format_exc(e)
        time.sleep(1)
        downloader(url=url)
        count += 1
