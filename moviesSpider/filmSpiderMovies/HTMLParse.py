# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
from DataOut import DataWrite
from URLDownloader import Download


class Parse(object):
    def __init__(self):
        self.down = Download()
        self.write = DataWrite()

    def pages_parse(self, movie_url):
        web_data = self.down.downloader(url=movie_url)

        soup = BeautifulSoup(markup=web_data, features="lxml")

        title = soup.find(name="h1", attrs={"class": "fw f24 fst pl10"})
        if title:
            title = title.text.strip()
            print title

        director_actor = soup.find(name="span", attrs={"class": "fs0 fl w440 wb"})
        if director_actor:
            director_actor_list = director_actor.text.strip().split("/")
            director = director_actor_list[0].strip()
            actors = ",".join([actor.strip() for actor in director_actor_list[1:]])
            print director
            print actors

        movie_type = soup.find(name="span", attrs={"class": "fs0 w440 fl"})
        if movie_type:
            movie_type = ",".join([temp.strip() for temp in movie_type.text.strip().split(" ")])
            print movie_type

        movieID = re.compile(r'http://film.spider.com.cn/film-(\S+)/').findall(string=movie_url)
        if movieID:
            print movieID[0]

        data = {
            "name": title,
            "web": u"蜘蛛电影",
            "movie_type": movie_type,
            "director": director,
            "local": "null",
            "movieID": movieID[0],
            "actor": actors
        }

        self.write.write(data=data)

    def get_movie_url(self, web_data):

        movie_url_list = []

        if not web_data:
            print "web_data error"
            return

        soup = BeautifulSoup(markup=web_data, features="lxml")

        res_movie_pic_div = soup.find_all(name="div", attrs={"class": "res_movie_pic"})
        if res_movie_pic_div:
            for res_movie in res_movie_pic_div:
                href = res_movie.contents[1].attrs["href"]
                print href
                movie_url_list.append(href)

        if movie_url_list:
            return movie_url_list
