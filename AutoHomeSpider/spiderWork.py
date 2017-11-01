# -*- coding: utf-8 -*-


import threadpool
import Queue
import os
import time
from carInfo import CarInfoParser
from htmlParser import HTMLParser


def start_work(q):
    index_list = []

    info_parse = CarInfoParser()

    print "work start."
    while (not q.empty()):
        for i in xrange(20):
            try:
                index_list.append(q.get(timeout=1))
            except Exception as e:
                print "Queue get url timeout."
                break

        print len(index_list)
        pool = threadpool.ThreadPool(len(index_list))
        requests = threadpool.makeRequests(info_parse.carParser, index_list)
        [pool.putRequest(req) for req in requests]
        pool.wait()
        index_list = []
        time.sleep(60)
    print "get all urls done."


if __name__ == '__main__':

    poll_times = 0

    html_parse = HTMLParser()
    q = Queue.Queue()

    if os.path.exists("URL.txt"):
        print "get url from URL.txt"
        with open(name="URL.txt", mode="r") as f:
            map(lambda x: q.put(x), f)
            os.remove("URL.txt")
        start_work(q=q)
    else:
        html_parse.parser_tit_tag()
        with open(name="URL.txt", mode="r") as f:
            map(lambda x: q.put(x), f)
            os.remove("URL.txt")
        start_work(q=q)