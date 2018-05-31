# -*- coding: utf-8 -*-

import time
from HTMLParse import Parse
from URLDownloader import Download


def work():
    p = Parse()
    d = Download()

    start_url_list = [
        "http://film.spider.com.cn/shangh-film----/",
        "http://film.spider.com.cn/shangh-film-----2/",
        "http://film.spider.com.cn/shangh-film-----3/",
        "http://film.spider.com.cn/shangh-film-----4/"
    ]

    for start_url in start_url_list:
        web_data = d.downloader(url=start_url)
        movies_list = p.get_movie_url(web_data=web_data)

        if movies_list:
            for movies in movies_list:
                p.pages_parse(movie_url=movies)
                print "sleep 10s"
                time.sleep(10)
        else:
            print "null movies_list"


work()
