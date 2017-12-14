# -*- coding: utf-8 -*-


import threadpool
import Queue
import os
import time
from carInfo import CarInfoParser
from htmlParser import HTMLParser
from myRedis import MyRedis


def start_work(db, num):
    redis = MyRedis()

    info_parse = CarInfoParser()

    print "work start."
    while (redis.check_urls_number(db=db)):
        url_list = redis.get_urls(db=db, num=num)
        print len(url_list)
        pool = threadpool.ThreadPool(len(url_list))
        requests = threadpool.makeRequests(info_parse.carParser, url_list)
        [pool.putRequest(req) for req in requests]
        pool.wait()
        time.sleep(60)
    print "get all urls done."


if __name__ == '__main__':

    poll_times = 0

    html_parse = HTMLParser()
    html_parse.parser_tit_tag(db="autohomeInfo", new=False)

    start_work(db="autohomeInfo", num=5)