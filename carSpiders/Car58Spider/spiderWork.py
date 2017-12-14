# -*- coding: utf-8 -*-

import sys
import time
import threadpool
from htmlParser import HTMLParser
from myRedis import MyRedis
from carInfo import CarInfoParser


def start_work(db, num, additional):
    info_parse = CarInfoParser()
    r = MyRedis(db, additional)
    html_parse = HTMLParser(db=db)

    if not r.check_urls_number():
        html_parse.get_brand_url(url="http://www.58che.com/all.html")

    while (r.check_urls_number()):
        urls_list = r.get_urls(num=num)
        print len(urls_list)
        pool = threadpool.ThreadPool(len(urls_list))
        requests = threadpool.makeRequests(info_parse.car_info_parse, urls_list)
        [pool.putRequest(req) for req in requests]
        pool.wait()
        print "sleep 5S"
        sys.stdout.flush()
        time.sleep(5)

    print "get all urls done."


if __name__ == '__main__':
    start_work(db="car58Info", num=10, additional=True)
