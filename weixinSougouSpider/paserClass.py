# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
from weixinSougouSpider.URLDownloader import downloader
from weixinSougouSpider.dataOut import writeData

class Paser(object):

    def __init__(self):
        self.parttern = re.compile(r'"content_url":"(\S+?)"')

    def parse_links(self, url, operator):
        web_data = downloader(url)
        if web_data:
            soup = BeautifulSoup(markup=web_data, features="lxml")
            link = soup.find(name="a", attrs={"uigs": "account_name_0"})
            if link:
                self.parse_item(url=link.attrs["href"], operator=operator)

    def parse_item(self, url, operator):
        web_data = downloader(url)
        if web_data:

            soup = BeautifulSoup(markup=web_data, features="lxml")
            scripts = soup.find_all(name="script", attrs={"type": "text/javascript"})
            print scripts
            for script in scripts:
                if "var msgList = " in str(script):
                    url_list = self.parttern.findall(string=str(script))

                    if url_list:
                        for url in url_list:
                            new_web_data = downloader(url=url)

                            if new_web_data:
                                soup = BeautifulSoup(markup=new_web_data, features="lxml")
                                title = soup.find(name="h2", attrs={"id": "activity-name"}).text
                                time = soup.find(name="em", attrs={"id": "post-date"}).text
                                contents = soup.find(name="div", attrs={"class": "rich_media_content "}).text
                                public_name = soup.find(name="a", attrs={"id": "post-user"}).text

                                data = {
                                    "title": title,
                                    "time": time,
                                    "contents": contents,
                                    "public": public_name,
                                    "url": url
                                }

                                writeData(data, operator)
