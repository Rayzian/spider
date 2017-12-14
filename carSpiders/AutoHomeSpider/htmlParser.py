# -*- coding: utf-8 -*-

import Queue
import re
from bs4 import BeautifulSoup
from URLDownloader import downloader
from myRedis import MyRedis


class HTMLParser(object):
    def __init__(self):
        self.redis = MyRedis()
        self.q = Queue.Queue()
        self.pattern = re.compile(r'a href="(//www.autohome.com.cn/\d+/#\w+=\w+&\w+=\d+)"')

    def parser_tit_tag(self, db, new):
        if new:
            for temp_url in ["https://www.autohome.com.cn/grade/carhtml/%s.html" % unichr(index) for index in
                             xrange(0x41, 0x5B)]:
                data = downloader(temp_url)
                if data:

                    links = re.findall(pattern=self.pattern, string=data)
                    for link in links:
                        link = "https:" + link
                        self.q.put(link)
                        self.q.task_done()

                    self.redis.save_urls(db=db, q=self.q, new=new)

        # if not self.q.empty():
        #     return self.q


# html = HTMLParser()
# html.parser_tit_tag()