# -*- coding: utf-8 -*-

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
        print "sleep 30S"
        time.sleep(30)

    print "get all urls done."


if __name__ == '__main__':

    # car_type_url_dict = {
    #     u"微型": "http://select.car.yiche.com/selectcartool/searchresult?l=1&external=Car&v=20171011&callback=jsonpCallback",
    #     u"小型": "http://select.car.yiche.com/selectcartool/searchresult?l=2&external=Car&v=20171011&callback=jsonpCallback",
    #     u"紧凑型": "http://select.car.yiche.com/selectcartool/searchresult?l=3&external=Car&v=20171011&callback=jsonpCallback",
    #     u"中型": "http://select.car.yiche.com/selectcartool/searchresult?l=5&external=Car&v=20171011&callback=jsonpCallback",
    #     u"中大型": "http://select.car.yiche.com/selectcartool/searchresult?l=4&external=Car&v=20171011&callback=jsonpCallback",
    #     u"豪华型": "http://select.car.yiche.com/selectcartool/searchresult?l=6&external=Car&v=20171011&callback=jsonpCallback",
    #     u"MPV": "http://select.car.yiche.com/selectcartool/searchresult?l=7&external=Car&v=20171011&callback=jsonpCallback",
    #     u"小型SUV": "http://select.car.yiche.com/selectcartool/searchresult?l=13&external=Car&v=20171011&callback=jsonpCallback",
    #     u"紧凑型SUV": "http://select.car.yiche.com/selectcartool/searchresult?l=14&external=Car&v=20171011&callback=jsonpCallback",
    #     u"中型SUV": "http://select.car.yiche.com/selectcartool/searchresult?l=15&external=Car&v=20171011&callback=jsonpCallback",
    #     u"中大型SUV": "http://select.car.yiche.com/selectcartool/searchresult?l=16&external=Car&v=20171011&callback=jsonpCallback",
    #     u"全尺寸SUV": "http://select.car.yiche.com/selectcartool/searchresult?l=17&external=Car&v=20171011&callback=jsonpCallback",
    #     u"跑车": "http://select.car.yiche.com/selectcartool/searchresult?l=9&external=Car&v=20171011&callback=jsonpCallback",
    #     u"面包车": "http://select.car.yiche.com/selectcartool/searchresult?l=11&external=Car&v=20171011&callback=jsonpCallback",
    #     u"皮卡": "http://select.car.yiche.com/selectcartool/searchresult?l=12&external=Car&v=20171011&callback=jsonpCallback",
    #     u"客车": "http://select.car.yiche.com/selectcartool/searchresult?l=18&external=Car&v=20171011&callback=jsonpCallback",
    # }

    # for car_type_url in car_type_url_dict.keys():
    start_work(db="yicheInfo", num=10, additional=True)



