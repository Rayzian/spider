# -*- coding: utf-8 -*-

import sys
import time
import threadpool
from getCarURL import CarURLParse
from myRedis import MyRedis
from carInfo import car_parser


def start_work(db, num, additional):
    r = MyRedis(db, additional)
    html_parse = CarURLParse(db=db, additional=additional)

    if not r.check_urls_number():
        html_parse.start_parser()
        print "sleep 180s before start parser"
        time.sleep(180)

    while (r.check_urls_number()):
        urls_list = r.get_urls(num=num)
        print len(urls_list)
        pool = threadpool.ThreadPool(len(urls_list))
        requests = threadpool.makeRequests(car_parser, urls_list)
        [pool.putRequest(req) for req in requests]
        pool.wait()
        print "sleep 5S"
        sys.stdout.flush()
        time.sleep(5)

    print "get all urls done."


if __name__ == '__main__':

    start_work(db="renrenInfo", num=10, additional=True)