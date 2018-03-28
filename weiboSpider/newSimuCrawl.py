# coding=utf-8

"""
All rights Reserved, Designed By Mign.cn
Title ： simuCrawl.py
Description : 运营商微博文章爬虫
Author : chenjide
Changed: zhouxiaoxi
Date : 2018年2月4日
Version : 0.1
"""

import Queue
import re
import codecs
import signal
import datetime
import os
from selenium import webdriver
import time
import traceback
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import sys

reload(sys)
sys.setdefaultencoding('utf8')


class Crawler(object):
    def __init__(self):
        self.browser = webdriver.Firefox(executable_path="/bin/geckodriver")

        self.browser.implicitly_wait(30)
        self.browser.set_page_load_timeout(90)

    def start(self, data, date, floder_path):

        self.browser.get(data["url"])
        time.sleep(15)

        try:
            # self.login()
            self.parse(data=data, date=date, floder_path=floder_path)
        except Exception as e:
            print e
            self.browser.close()

    def parse(self, date, floder_path, data, count=1):
        # 开始滑到最底
        time.sleep(5)
        for i in range(10):
            self.browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            time.sleep(3)
        try:
            elements = self.browser.find_elements_by_class_name('WB_detail')
            feed_handles = self.browser.find_elements_by_class_name("WB_feed_handle")
            for element, handle in zip(elements, feed_handles):
                try:
                    transpond_num = handle.find_element_by_xpath(
                        './/div[@class="WB_handle"]/ul/li[2]/a/span/span/span/em[2]').text.encode(
                        'utf-8').strip().replace("\n", "")

                    comment_num = handle.find_element_by_xpath(
                        './/div[@class="WB_handle"]/ul/li[3]/a/span/span/span/em[2]').text.encode(
                        'utf-8').strip().replace("\n", "")

                    likes_num = handle.find_element_by_xpath(
                        './/div[@class="WB_handle"]/ul/li[4]/a/span/span/span/em[2]').text.encode(
                        'utf-8').strip().replace("\n", "")

                    time_num = element.find_element_by_xpath(
                        './/div[@class="WB_from S_txt2"]/a[1]').text.encode('utf-8').strip().replace("\n", "")

                    Name = element.find_element_by_xpath('.//div[@class="WB_info"]/a[1]').text.encode(
                        'utf-8').strip().replace("\n", "")

                    content = element.find_element_by_xpath('.//div[@class="WB_text W_f14"]').text.encode(
                        'utf-8').strip().replace("\n", "")

                    tags = re.compile(r'#\S+#').findall(string=content)[0] if re.compile(r'#\S+#').findall(
                        string=content) else "NULL"

                    line = time_num + "\001" + Name + "\001" + content + "\001" + tags + "\001" + transpond_num + "\001" + comment_num + "\001" + likes_num + "\n"
                    print line
                    try:
                        stri = "WeiBo_%s_info_%s.txt" % (data["operator"], date)
                        path = os.path.join(floder_path, stri)
                        file_write = open(path, 'a')
                        file_write.write(line)
                    except Exception:
                        print '文件写出失败', traceback.print_exc()
                except Exception as e:
                    print e
        except Exception as err:
            # 没有找到输入框，说明已经登录过
            self.browser.close()
            return
        if count < 3:
            self.check_nextPage(date=date, floder_path=floder_path, data=data, count=count)
        self.browser.close()

    def login(self):

        login_buton = self.browser.find_element_by_xpath(".//*[@id='pl_common_top']/div/div/div[3]/div[2]/ul/li[3]/a")
        login_buton.click()
        time.sleep(10)

        self.browser.switch_to_alert()
        time.sleep(3)

        account = self.browser.find_element_by_name("username")
        account.clear()
        account.send_keys("x")
        time.sleep(1)

        password = self.browser.find_element_by_name("password")
        password.clear()
        password.send_keys("x")
        time.sleep(1)

        confirm = self.browser.find_element_by_xpath(
            ".//div[@class='layer_login_register_v2 clearfix']/div[3]/div[6]/a")
        confirm.click()
        time.sleep(30)

    def check_nextPage(self, date, floder_path, data, count):
        try:
            if str(self.browser.find_element_by_xpath(".//div[@class='W_pages']/a").text) == "下一页":
                print self.browser.find_element_by_xpath(".//div[@class='W_pages']/a").text
                self.browser.find_element_by_xpath(".//div[@class='W_pages']/a").click()

                time.sleep(10)
                count += 1
                self.parse(date=date, floder_path=floder_path, data=data, count=count)
            elif str(self.browser.find_element_by_xpath(".//div[@class='W_pages']/a[2]").text) == "下一页":
                print self.browser.find_element_by_xpath(".//div[@class='W_pages']/a[2]").text
                self.browser.find_element_by_xpath(".//div[@class='W_pages']/a[2]").click()
                time.sleep(10)
                count += 1
                self.parse(date=date, floder_path=floder_path, data=data, count=count)
        except Exception as e:
            if str(self.browser.find_element_by_xpath(".//div[@class='W_pages']/a[2]").text) == "下一页":
                print self.browser.find_element_by_xpath(".//div[@class='W_pages']/a[2]").text
                self.browser.find_element_by_xpath(".//div[@class='W_pages']/a[2]").click()
                time.sleep(10)
                count += 1
                self.parse(date=date, floder_path=floder_path, data=data, count=count)

        finally:
            return


if __name__ == '__main__':
    print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<开始浏览器模拟内容>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"

    q = Queue.Queue()

    date = datetime.datetime.now().strftime('%Y_%m_%d')
    floder_path = r"/data/yuqing/weibo"
    time.sleep(1)

    public_type = {
        "liantong": r"/data/yuqing/weibo/weiboYuQingSpider/weiboPublic_url_liantongs.txt",
        "dianxin": r"/data/yuqing/weibo/weiboYuQingSpider/weiboPublic_urls_dianxin.txt",
        "yidong": r"/data/yuqing/weibo/weiboYuQingSpider/weiboPublic_urls_yidong.txt"
    }

    for operator in public_type.keys():
        with open(name=public_type[operator], mode="r") as ff:
            for temp in ff:
                url = temp.strip().split("|")[-1].strip()
                data = {
                    "operator": operator,
                    "url": url
                }
                q.put(data, timeout=5)
        time.sleep(3)

    while (not q.empty()):
        try:
            public_data = q.get(timeout=5)

            print public_data

            c = Crawler()
            c.start(data=public_data, date=date, floder_path=floder_path)
        except Exception as e:
            try:
                err_file_name = "/data/yuqing/weibo/weiboYuQingSpider/log/%s_failed_log.txt" % date
                err_content = "%s\n%s\n" % (public_data, traceback.format_exc(e))
                with codecs.open(filename=err_file_name, mode="a+", encoding="utf-8") as ef:
                    ef.write(err_content)
            except:
                pass

        print "sleep 60s"
        time.sleep(60)
