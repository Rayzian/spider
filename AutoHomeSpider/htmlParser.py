# -*- coding: utf-8 -*-

import Queue
import re
from bs4 import BeautifulSoup
from AutoHomeSpider.URLDownloader import downloader


class HTMLParser(object):
    def __init__(self):
        self.q = Queue.Queue()
        self.pattern = re.compile(r'a href="(//www.autohome.com.cn/\d+/#\w+=\w+&\w+=\d+)"')

    def parser_tit_tag(self):
        for temp_url in ["https://www.autohome.com.cn/grade/carhtml/%s.html" % unichr(index) for index in
                         xrange(0x41, 0x5B)]:
            data = downloader(temp_url)
            if data:

                links = re.findall(pattern=self.pattern, string=data)
                for link in links:
                    link = "https:" + link
                    # self.q.put(link)
                    # self.q.task_done()
                    with open("URL.txt", mode="a") as f:
                        f.write(link)
                        f.write("\n")
                    print "put %s into queue: " % link

        # if not self.q.empty():
        #     return self.q


# html = HTMLParser()
# html.parser_tit_tag()