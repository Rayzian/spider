# -*- coding: utf-8 -*-

import time
import json
from bs4 import BeautifulSoup
from URLDownloader import dowoloader
from DateOut import DataWrite


class parser(object):
    def __init__(self):
        self.down = dowoloader()

    def parse_json_api(self, web_data):

        if not web_data:
            return

        web_data_split = web_data.strip().split("=", 1)[1].strip().split(";", 1)[0].strip()

        web_data_json = json.loads(web_data_split)

        movies_list = [movies_data for movies_data in web_data_json["value"]["movies"]]

        if movies_list:
            return movies_list
        else:
            return False

    def parse_movie_info(self, movieID, name):

        time.sleep(10)
        url = "http://movie.mtime.com/{movieID}/".format(movieID=movieID)
        web_data = self.down.pages_download(url=url)

        if not web_data:
            print "no pages web_data"
            return

        soup = BeautifulSoup(markup=web_data, features="lxml")

        movie_type_list = soup.find_all(name="div", attrs={"class": "otherbox __r_c_"})
        if movie_type_list:
            movie_type = movie_type_list[0].text.strip().split("-")[1].strip().replace("/", ",")

        info_l_list = soup.find_all(name="dl", attrs={"class": "info_l"})
        if info_l_list:
            director = info_l_list[0].contents[1].contents[2].text.strip()
            local = info_l_list[0].contents[5].contents[3].text.strip()

        data = {
            "name": name,
            "web": u"时光网",
            "movie_type": movie_type,
            "director": director,
            "local": local,
            "movieID": movieID,
            "actor": ""
        }

        self.parser_actor_info(data=data, movieID=movieID)

    def parser_actor_info(self, data, movieID):

        actor_url = "http://movie.mtime.com/{movieID}/fullcredits.html".format(movieID=movieID)
        print actor_url

        actor_web_data = self.down.pages_download(url=actor_url)

        if not actor_web_data:
            return

        soup = BeautifulSoup(markup=actor_web_data, features="lxml")

        db_actor_div = soup.find(name="div", attrs={"class": "db_actor"})
        if db_actor_div:
            actor_list = soup.find_all(name="div", attrs={"class": "actor_tit"})
            actors_list = []
            if actor_list:
                for actor in actor_list[1:]:
                    try:
                        actors = actor.contents[1].contents[3].text.strip()
                    except:
                        actors = actor.contents[1].text.strip()
                    actors_list.append(actors)

                data["actor"] = ",".join(actors_list)

        if data["actor"] != "":
            w = DataWrite()
            w.write(data)
