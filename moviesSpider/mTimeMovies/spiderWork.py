# -*- coding: utf-8 -*-

import time
from HTMLParse import parser
from URLDownloader import dowoloader


def work():
    download = dowoloader()
    p = parser()
    start_url = "http://service.theater.mtime.com/Cinema.api?Ajax_CallBack=true&Ajax_CallBackType=Mtime.Cinema.Services&Ajax_CallBackMethod=GetOnlineMoviesInCity&Ajax_CrossDomain=1&Ajax_RequestUrl=http%3A%2F%2Ftheater.mtime.com%2FChina_Sichuan_Province_Chengdu%2F&t=2018529&Ajax_CallBackArgument0=880"

    api_web_data = download.get_movies(url=start_url)
    if not api_web_data:
        print "api_web_data is null"
        return

    movies_list_dict = p.parse_json_api(web_data=api_web_data)

    for movies_dict in movies_list_dict:
        print movies_dict
        p.parse_movie_info(movieID=movies_dict["movieId"], name=movies_dict["title"])
        print "sleep 60s"
        time.sleep(60)


work()
