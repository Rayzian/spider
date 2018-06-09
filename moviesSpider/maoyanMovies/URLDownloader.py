# -*- coding: utf-8 -*-

import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def download(url, render=False):
    desired_capabilities = dict(DesiredCapabilities.PHANTOMJS)

    desired_capabilities["phantomjs.page.settings.userAgent"] = (
        'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0')

    browser = webdriver.PhantomJS(
        executable_path=r'/Users/zhouxiaoxi/Downloads/phantomjs-2.1-2.1-macosx/bin/phantomjs',
        desired_capabilities=desired_capabilities)
    # browser = webdriver.PhantomJS(executable_path=r'E:\phantomjs-2.1.1-windows\bin\phantomjs.exe',
    #                               desired_capabilities=desired_capabilities)

    browser.implicitly_wait(20)
    browser.set_page_load_timeout(60)

    browser.get(url=url)

    if render:
        try:
            more = browser.find_element_by_class_name(name="more")
            more.click()
            time.sleep(10)
            text = browser.page_source
            browser.close()
            return text
        except:
            text = browser.page_source
            browser.close()
            return text
    text = browser.page_source
    browser.close()
    return text
