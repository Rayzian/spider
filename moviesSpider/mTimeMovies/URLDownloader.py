# -*- coding: utf-8 -*-

import time
import requests
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class dowoloader(object):
    def get_movies(self, url):

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:52.0) Gecko/20100101 Firefox/52.0",
            "Referer": "http://theater.mtime.com/China_Sichuan_Province_Chengdu/",
            "Host": "service.theater.mtime.com"
        }

        s = requests.Session()
        web_data = s.get(url=url, headers=headers)

        if web_data.status_code == 200:
            return web_data.text
        else:
            return False

    def pages_download(self, url):
        desired_capabilities = dict(DesiredCapabilities.PHANTOMJS)

        desired_capabilities["phantomjs.page.settings.userAgent"] = (
            'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0')

        browser = webdriver.PhantomJS(
            executable_path=r'/Users/zhouxiaoxi/Downloads/phantomjs-2.1-2.1-macosx/bin/phantomjs',
            desired_capabilities=desired_capabilities)

        browser.implicitly_wait(20)
        browser.set_page_load_timeout(60)

        browser.get(url=url)

        time.sleep(5)

        text = browser.page_source
        browser.close()

        return text
