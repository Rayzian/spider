# -*- coding: utf-8 -*-

import time
import threading
import Queue
from carInfo import CarInfoParser
from htmlParser import HTMLParser

if __name__ == '__main__':
    # local_id_dict = {
    #     "beijing": "110000/110100",
    #     "shanghai": "310000/310100",
    #     "guangzhou": "440000/440100",
    #     "shenzhen": "440000/440300"
    # }

    info_parse = CarInfoParser()
    html_parse = HTMLParser()
    url_q = html_parse.parser_tit_tag()

    print "work start."
    # for city in local_id_dict.keys():
    while (not url_q.empty()):
        url_1 = None
        url_2 = None
        url_3 = None
        url_4 = None
        try:
            url_1 = url_q.get(True, timeout=3)
            print "get url: ", url_1
            url_2 = url_q.get(True, timeout=3)
            print "get url: ", url_2
            url_3 = url_q.get(True, timeout=3)
            print "get url: ", url_3
            url_4 = url_q.get(True, timeout=3)
            print "get url: ", url_4
        except Queue.Empty:
            print "Queue is empty."

        if url_1 and url_2 and url_3 and url_4:
            th1 = threading.Thread(target=info_parse.carParser, args=(url_1,),
                                   name="thread1")
            th2 = threading.Thread(target=info_parse.carParser, args=(url_2,),
                                   name="thread2")
            th3 = threading.Thread(target=info_parse.carParser, args=(url_3,),
                                   name="thread3")
            th4 = threading.Thread(target=info_parse.carParser, args=(url_4,),
                                   name="thread4")

            th1.start()
            time.sleep(0.5)
            th2.start()
            time.sleep(0.5)
            th3.start()
            time.sleep(0.5)
            th4.start()
            time.sleep(0.5)

            th1.join()
            th2.join()
            th3.join()
            th4.join()

        else:
            if url_1:
                th1 = threading.Thread(target=info_parse.carParser, args=(url_1,),
                                       name="thread1")
                th1.start()
                time.sleep(0.5)
                th1.join()
            if url_2:
                th2 = threading.Thread(target=info_parse.carParser, args=(url_2,),
                                       name="thread2")
                th2.start()
                time.sleep(0.5)
                th2.join()
            if url_3:
                th3 = threading.Thread(target=info_parse.carParser, args=(url_3,),
                                       name="thread3")
                th3.start()
                time.sleep(0.5)
                th3.join()
            if url_4:
                th4 = threading.Thread(target=info_parse.carParser, args=(url_4,),
                                       name="thread4")
                th4.start()
                time.sleep(0.5)
                th4.join()
