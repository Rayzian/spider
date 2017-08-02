# -*- coding: utf-8 -*-

import json
import scrapy
from scrapy import Request, FormRequest

class ZhihucrawlSpider(scrapy.Spider):
    name = "zhihuCrawl"
    allowed_domains = ["zhihu.com"]
    start_urls = (
        'http://www.zhihu.com/',
    )

    def start_requests(self):
        return [Request(url="https://www.zhihu.com/#signin",
                        callback=self.start_login,
                        meta={"cookiejar": 1})
                ]

    def start_login(self, response):
        self.xsrf = response.xpath("//input[@name='_xsrf']/@value").extract()
        return [FormRequest(url="https://www.zhihu.com/login/phone_num",
                            method="POST",
                            meta={"cookiejar": response.meta["cookiejar"]},
                            formdata={
                                "_xsrf": str(self.xsrf),
                                "captcha_type": "cn",
                                "password": "x",
                                "phone_num": "x"
                            },
                            callback=self.after_login)]


    def after_login(self, response):
        if json.loads(response.body)["msg"].encode("utf8") == "登录成功":
            self.logger.info(str(response.meta["cookiejar"]))
            print "login successed."


    # def parse(self, response):
    #     pass
