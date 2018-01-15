# -*- coding: utf-8 -*-

import sys
import time
import threadpool
from getCarURL import htmlParser
from myRedis import MyRedis
from carInfo import CarParser


def start_work(db, num, additional):
    info_parse = CarParser()
    r = MyRedis(db, additional)
    html_parse = htmlParser(db=db)

    if not r.check_urls_number():
        html_parse.get_brand_url()
        print "Save urls done. sleep 120S"
        time.sleep(120)

    while (r.check_urls_number()):
        urls_list = r.get_urls(num=num)
        print len(urls_list)
        pool = threadpool.ThreadPool(len(urls_list))
        requests = threadpool.makeRequests(info_parse.car_info, urls_list)
        [pool.putRequest(req) for req in requests]
        pool.wait()
        print "sleep 5S"
        sys.stdout.flush()
        time.sleep(5)

    print "get all urls done."


if __name__ == '__main__':
    start_work(db="pcautoInfo", num=5, additional=True)
