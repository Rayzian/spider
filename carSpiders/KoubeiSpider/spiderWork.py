# -*- coding: utf-8 -*-

import sys
import time
import threadpool
from getCarURL import URLParser
from myRedis import MyRedis
from carInfo import CarParser


def start_work(db, num, additional):
    info_parse = CarParser()
    r = MyRedis(db, additional)
    html_parse = URLParser(db=db)

    if not r.check_urls_number():
        html_parse.start_parser()
        print "get all url done, sleep 120S"
        time.sleep(120)

    while (r.check_urls_number()):
        urls_list = r.get_urls(num=num)
        print len(urls_list)
        # pool = threadpool.ThreadPool(len(urls_list))
        # requests = threadpool.makeRequests(info_parse.car_info, urls_list)
        # [pool.putRequest(req) for req in requests]
        # pool.wait()
        # print "sleep 3S"
        # sys.stdout.flush()
        # time.sleep(3)
        info_parse.car_info(car_info=urls_list[0])
        print "sleep 1S"
        sys.stdout.flush()
        time.sleep(1)
    print "get all urls done."


if __name__ == '__main__':
    start_work(db="koubeiInfo", num=1, additional=True)
