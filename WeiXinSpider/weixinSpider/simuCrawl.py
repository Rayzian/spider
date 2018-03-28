# -*- coding: utf-8 -*-
"""
All rights Reserved, Designed By Mign.cn
Title ： simuCrawl.py
Crawler Purposes : 爬取中国移动、中国电信、中国联通微信公众号文章。
Describe : 爬取网站为新榜（https://www.newrank.cn），公众号链接为https://www.newrank.cn/public/login/login.html?isDetail=1&detailAccount=xxx。
           爬取流程：
                   1）、使用selenium + phantomjs加载js，获取网页标签解析爬取目标信息；使用redis集合作为任务队列存储公众号ID
                   2）、登陆账号
                   3）、获取最新文章标签，有标签则获取文章链接，输出公众号文章；无则退出该公众号网页
Author : zhouxiaoxi
Date : 2018.2.1
Version : 1.0

"""

import time
from myRedis import MyRedis
from dataOut import writeData
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import sys

reload(sys)
sys.setdefaultencoding('utf8')


class TaskWork(object):
    def __init__(self):
        desired_capabilities = dict(DesiredCapabilities.PHANTOMJS)
        desired_capabilities["phantomjs.page.settings.loadImages"] = False
        desired_capabilities["phantomjs.page.settings.userAgent"] = (
            'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0')

        self.driver = webdriver.PhantomJS(executable_path=r"/usr/local/bin/phantomjs",
                                          desired_capabilities=desired_capabilities)

        self.driver.implicitly_wait(30)
        self.driver.set_page_load_timeout(60)

    def crawl(self, date, public_data):
        try:
            print "start crawl..."

            url = "https://www.newrank.cn/public/login/login.html?isDetail=1&detailAccount=%s" % public_data["public"]
            print "keys %s" % public_data["public"]
            print "%s" % url
            self.driver.get(url=url)
            obj = self.driver.find_element_by_xpath("html/body/div[2]/div/div[1]/div[1]/div[2]")
            obj.click()
            time.sleep(3)

            user = self.driver.find_element_by_xpath(".//*[@id='account_input']")
            user.clear()
            user.send_keys(["17381540262"])
            time.sleep(1)

            password = self.driver.find_element_by_xpath(".//*[@id='password_input']")
            password.clear()
            password.send_keys(["password11415269"])
            time.sleep(1)

            login_button = self.driver.find_element_by_xpath(".//*[@id='pwd_confirm']")
            login_button.click()
            time.sleep(10)

            soup = BeautifulSoup(markup=self.driver.page_source, features="lxml")
            new_artcles_list = soup.find(name="ul", attrs={"id": "info_detail_article_lastest"})
            if new_artcles_list:
                for new_atrcles in new_artcles_list.contents:
                    public_url = new_atrcles.contents[0].contents[0].attrs["href"]
                    public_read = new_atrcles.contents[2].contents[2].contents[1].text.strip() if \
                        new_atrcles.contents[2].contents[2].contents[1] else "0"
                    public_like = new_atrcles.contents[2].contents[2].contents[2].text.strip() if \
                        new_atrcles.contents[2].contents[2].contents[2] else "0"

                    self.driver.get(url=public_url)
                    time.sleep(5)
                    soup = BeautifulSoup(markup=self.driver.page_source, features="lxml")
                    page_time = soup.find(name="em", attrs={"class": "rich_media_meta rich_media_meta_text"})
                    public_name = soup.find(name="a",
                                            attrs={
                                                "class": "rich_media_meta rich_media_meta_link rich_media_meta_nickname"})
                    title = soup.find(name="h2", attrs={"class": "rich_media_title"})
                    text_content = soup.find(name="div", attrs={"class": "rich_media_content "})

                    if page_time and public_name and title and text_content:
                        data = {
                            "time": page_time.text.strip(),
                            "name": public_name.text.strip(),
                            "title": title.text.strip(),
                            "content": text_content.text.strip(),
                            "reprint": "0",
                            "comment": "0",
                            "public_like": public_like,
                            "public_read": public_read
                        }

                        writeData(data=data, date=date, operator=public_data["operator"])
                        print "sleep 15S"
                        time.sleep(15)

                self.driver.quit()
                return
            else:
                self.driver.quit()
                return

        except Exception as e:
            print e
            self.driver.quit()
            return


if __name__ == '__main__':

    date = time.strftime('%Y_%m_%d', time.localtime(time.time()))

    r = MyRedis(db="weixinpub_info", new=True)
    if not r.check_urls_number():

        public_type = {
            "liantong": r"/data/yuqing/weixin/weixinSpider/liantong.txt",
            "dianxin": r"/data/yuqing/weixin/weixinSpider/dianxin.txt",
            "yidong": r"/data/yuqing/weixin/weixinSpider/yidong.txt"
        }
        for operator in public_type.keys():
            with open(name=public_type[operator], mode="r") as ff:
                for temp in ff:
                    public = temp.strip().split("|")[-1].strip()
                    data = {
                        "operator": operator,
                        "public": public
                    }
                    r.save_urls(company_name=data)

    while (r.check_urls_number()):
        public_data = eval(r.get_urls()[0])
        print public_data

        try:
            task = TaskWork()
            task.crawl(date=date, public_data=public_data)
        except Exception as e:
            print e
        print "sleep 60S"
        time.sleep(60)
