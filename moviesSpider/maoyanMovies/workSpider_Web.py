# -*- coding: utf-8 -*-

import traceback
import time
from HTMLParse import Parse
from URLDownloader import download
from myRedis import MyRedis


def start_work(fun1, fun2):
    while (fun1.check_urls_number()):
        url = fun1.get_urls()
        print url
        if url:
            try:
                web_data = download(url=url, render=True)
                fun2.page_parse(web_data=web_data, url=url)
            except Exception as e:
                print traceback.format_exc(e)

        print "sleep 15S"
        time.sleep(15)

    print "get all urls done."


if __name__ == '__main__':
    year_id_dict = {
        "14": 4,
        "13": 32
    }
    first_url = "http://maoyan.com/films?yearId={yearId}"
    next_url = "http://maoyan.com/films?yearId={yearId}&offset={offset}"

    db = "maoyan"
    additional = True
    r = MyRedis(db=db, additional=additional)
    parse = Parse()
    if not r.check_urls_number():
        for year_id in year_id_dict.keys():
            index = year_id_dict[year_id]
            for temp in range(int(index)):
                if temp == 0:
                    url = first_url.format(yearId=year_id)
                else:
                    url = next_url.format(yearId=year_id, offset=(int(temp) * 30))
                print url
                web_data = download(url=url)
                movie_url_list = parse.get_movies_url(web_data=web_data)
                map(lambda x: r.save_urls(x), movie_url_list)
                print "sleep 10s for get_movie_url"
                time.sleep(10)

    start_work(fun1=r, fun2=parse)
