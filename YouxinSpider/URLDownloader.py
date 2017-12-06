# -*- coding: utf-8 -*-

import re
import threading
import traceback
import codecs
import requests
import time
import cookielib
# from userAgent import user_agent
from bs4 import BeautifulSoup

lock = threading.Lock()
count = 0

cookie = None

headers = {
        'Host': 'www.xin.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:52.0) Gecko/20100101 Firefox/52.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
}

class myDownloader(object):
    def __init__(self):
        self.s = requests.Session()

    def downloader(self, url):
        global cookie
        get_url = ""
        global count
        if count > 3:
            with codecs.open(filename="failedUrl.txt", mode="a", encoding="utf-8") as fail:
                fail.write(str(url))
                fail.write("\n")

            print "Failed requests ", url
            count = 0
            # lock.release()
            return None

        try:
            # lock.acquire()
            # time.sleep(1)

            if isinstance(url, dict):
                get_url = url["car_url"]
            elif isinstance(url, str):
                get_url = url
            web_data = self.s.get(url=get_url, headers=headers, cookies=cookie)
            if web_data.status_code == 200:
                print "web_data.cookie: ", web_data.cookies.extract_cookies
                print "web_data.headers: ", web_data.headers
                soup = BeautifulSoup(markup=web_data.text, features="lxml")

                checker = soup.find(name="h3", attrs={"class": "title"}).text if soup.find(name="h3",
                                                                                           attrs={
                                                                                               "class": "title"}) else None
                if checker and u"人机交互校验" == checker:
                    print checker
                    # lock.release()
                    city_reg = "/%s/" % url["city"]
                    car_id = re.compile(r'%s(\w+)?\.html' % city_reg).findall(url["car_url"])[0]
                    vcode_url = "https://www.xin.com/checker/?redirect=%2F{city}%2F{car_id}.html%2F".format(
                        city=url["city"], car_id=car_id)
                    # vcode = raw_input("enter %s: " % vcode_url)
                    vcode = "qp9y"

                    payload = {"vcode": vcode}
                    self.s.post(url=vcode_url, data=payload, allow_redirects=True)
                    cookies = self.s.cookies
                    # global cookie
                    cookie = cookies
                    time.sleep(1)
                    web_data = self.s.get(url=get_url, headers=headers, cookies=cookie)
                    if web_data.status_code == 200:
                        print "Requests ", get_url, web_data
                        # lock.release()
                        cookies = self.s.cookies

                        cookie = cookies
                        return web_data.text

                print "Requests ", get_url, web_data
                # lock.release()
                # print web_data.text
                return web_data.text
            else:
                print get_url, web_data
                # lock.release()
                return

        except Exception as e:
            print traceback.format_exc(e)
            time.sleep(2)
            # lock.release()
            self.downloader(url=get_url)
            count += 1


# if __name__ == '__main__':
#     mytest_down = myDownloader()
#     url_dict = {
#         "city": "shenzhen",
#         "car_url": "https://www.xin.com/shenzhen/che30049607.html"
#     }
#
#     web = mytest_down.downloader(url=url_dict)