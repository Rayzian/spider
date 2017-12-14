# -*- coding: utf-8 -*-

import threading
import traceback
import codecs
import requests
import time

lock = threading.Lock()
count = 0

def downloader(url):
    get_url = ""
    global count
    if count > 3:
        with codecs.open(filename="failedUrl.txt", mode="a", encoding="utf-8") as fail:
            fail.write(str(url))
            fail.write("\n")

        print "Failed requests ", url
        count = 0
        lock.release()
        return None

    try:
        lock.acquire()
        headers = {
            'Host': 'www.guazi.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:52.0) Gecko/20100101 Firefox/52.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Cookie': 'cityDomain=sh; cainfo=%7B%22ca_s%22%3A%22pz_baidu%22%2C%22ca_n%22%3A%22tbmkbturl%22%2C%22ca_i%22%3A%22-%22%2C%22ca_medium%22%3A%22-%22%2C%22ca_term%22%3A%22-%22%2C%22ca_content%22%3A%22-%22%2C%22ca_campaign%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22keyword%22%3A%22-%22%2C%22ca_keywordid%22%3A%22-%22%2C%22scode%22%3A%2210103000312%22%2C%22platform%22%3A%221%22%2C%22version%22%3A1%2C%22client_ab%22%3A%22-%22%2C%22guid%22%3A%227f45f540-b7c4-49e0-ff40-5ceeeb29d590%22%2C%22sessionid%22%3A%22d8aea762-6b79-49a9-b3a1-62da6d37e562%22%7D; antipas=00s972321503702x9jT9076w690; uuid=7f45f540-b7c4-49e0-ff40-5ceeeb29d590; preTime=%7B%22last%22%3A1511417082%2C%22this%22%3A1511335463%2C%22pre%22%3A1511335463%7D; ganji_uuid=7455670864795263316801; lg=1; Hm_lvt_e6e64ec34653ff98b12aab73ad895002=1511335468,1511417074; clueSourceCode=%2A%2300; sessionid=d8aea762-6b79-49a9-b3a1-62da6d37e562; Hm_lpvt_e6e64ec34653ff98b12aab73ad895002=1511417083',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        }
        # proxies = proxy()
        session = requests.Session()
        # time.sleep(1)
        # web_data = session.get(url=url, headers=headers, proxies=proxies)
        if isinstance(url, dict):
            get_url = url["url"]
        elif isinstance(url, str):
            get_url = url
        web_data = session.get(url=get_url, headers=headers)
        if web_data.status_code == 200:
            try:
                print "Requests ", get_url, web_data
                lock.release()
                return web_data.text

            except:
                lock.release()
                return web_data
        else:
            print get_url, web_data
            lock.release()

    except Exception as e:
        print traceback.format_exc(e)
        time.sleep(2)
        lock.release()
        downloader(url=get_url)
        count += 1