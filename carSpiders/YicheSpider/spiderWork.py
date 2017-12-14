# -*- coding: utf-8 -*-

import time
import threadpool
from htmlParser import HTMLParser
from myRedis import MyRedis
from carParser import Parser


def start_work(db, num, additional):
    info_parse = Parser()
    r = MyRedis(db, additional)
    html_parse = HTMLParser(db=db, additional=additional)

    if not r.check_urls_number():
        html_parse.parse()
        print "sleep 180s before start parser"
        time.sleep(180)

    while (r.check_urls_number()):
        urls_list = r.get_urls(num=num)
        print len(urls_list)
        pool = threadpool.ThreadPool(len(urls_list))
        requests = threadpool.makeRequests(info_parse.car_parser, urls_list)
        [pool.putRequest(req) for req in requests]
        pool.wait()
        print "sleep 10S"
        time.sleep(10)

    print "get all urls done."


if __name__ == '__main__':

    start_work(db="yicheInfo", num=10, additional=True)




