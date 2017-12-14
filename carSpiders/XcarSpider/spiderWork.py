# -*- coding: utf-8 -*-

import time
import threadpool
from htmlParser import HTMLParser
from myRedis import MyRedis
from carInfo import CarInfo


def start_work(db, num, additional):
    info_parse = CarInfo()
    r = MyRedis(db, additional)
    html_parse = HTMLParser(db=db)

    
    if not r.check_urls_number():
        html_parse.get_car_detail_url()

    while(r.check_urls_number()):
        urls_list = r.get_urls(num=num)
        print len(urls_list)
        pool = threadpool.ThreadPool(len(urls_list))
        requests = threadpool.makeRequests(info_parse.car_parse, urls_list)
        [pool.putRequest(req) for req in requests]
        pool.wait()
        print "sleep 10S"
        time.sleep(10)

    print "get all urls done."


if __name__ == '__main__':
    start_work(db="xcarInfo", num=10, additional=True)



