# -*- coding: utf-8 -*-

import sys
import time
import threadpool
from htmlparser import HTMLParser
from myRedis import MyRedis
from carInfo import carParser


def start_work(db, num, additional):
    info_parse = carParser()
    r = MyRedis(db, additional)
    html_parse = HTMLParser(db=db)

    if not r.check_urls_number():
        html_parse.html_parser(url="http://car.autotimes.com.cn/ajax/brand.ashx")

    while (r.check_urls_number()):
        urls_list = r.get_urls(num=num)
        print len(urls_list)
        pool = threadpool.ThreadPool(len(urls_list))
        requests = threadpool.makeRequests(info_parse.car_parse, urls_list)
        [pool.putRequest(req) for req in requests]
        pool.wait()
        print "sleep 5S"
        sys.stdout.flush()
        time.sleep(5)

    print "get all urls done."


if __name__ == '__main__':
    start_work(db="cartimesInfo", num=5, additional=True)
