# -*- coding: utf-8 -*-

import traceback
from bs4 import BeautifulSoup
from DateOut import DataWrite
from myRedis import MyRedis


class Parse(object):
    def __init__(self):
        self.write = DataWrite()

    def get_movies_url(self, web_data):
        soup = BeautifulSoup(markup=web_data, features="lxml")

        movie_list = soup.find_all(name="div", attrs={"class": "channel-detail movie-item-title"})
        if movie_list:
            movie_url_list = ["http://maoyan.com" + str(movie.contents[1].attrs["href"].strip()) for movie in
                              movie_list]
            if movie_url_list:
                return movie_url_list

    def page_parse(self, web_data, url):

        movie_id = url.strip().split("/")[-1]

        soup = BeautifulSoup(markup=web_data, features="lxml")
        try:
            name = soup.find(name="h3", attrs={"class": "name"})
            if name:
                name = name.text.strip()

            ellipsis_list = soup.find_all(name="li", attrs={"class": "ellipsis"})
            if ellipsis_list:
                movie_type = ellipsis_list[0].text.strip()
                local = ellipsis_list[1].text.split("/")[0].strip()

            celebrity_container_div_list = soup.find_all(name="div", attrs={"class": "celebrity-container"})
            if celebrity_container_div_list:
                staff_type, staff = self.check_type(celebrity_container_div_list=celebrity_container_div_list)
                if staff_type == u"导演":
                    dircetor = staff
                    actor = ",".join([actors.text.strip().split("\n")[0].strip() for actors in
                                      celebrity_container_div_list[-1].contents[3].contents[3].contents if
                                      actors != "\n"])

                elif staff_type == u"演员":
                    dircetor = "null"
                    actor = staff

                else:
                    dircetor = "null"
                    actor = "null"

            print "%s %s %s %s %s" % (name, movie_type, local, dircetor, actor)

            data = {
                "name": name,
                "web": u"猫眼",
                "movie_type": movie_type,
                "director": dircetor,
                "local": local,
                "movieID": movie_id,
                "actor": actor
            }

            self.write.write(data=data)
        except Exception as e:
            print traceback.format_exc(e)

    def check_type(self, celebrity_container_div_list):
        try:
            if celebrity_container_div_list[-1].contents[1].contents[1].text.replace("\n", "").strip().split(" ")[
                0] != u"导演" and celebrity_container_div_list[-1].contents[1].contents[1].text.replace("\n",
                                                                                                      "").strip().split(
                " ")[0] != u"演员":
                return "null", "null"

            if celebrity_container_div_list[-1].contents[1].contents[1].text.replace("\n", "").strip().split(" ")[
                0] == u"导演":
                staff_type = u"导演"

            elif celebrity_container_div_list[-1].contents[1].contents[1].text.replace("\n", "").strip().split(" ")[
                0] == u"演员":
                staff_type = u"演员"

            staff = ",".join([dircetor.text.strip().split("\n")[0].strip() for dircetor in
                              celebrity_container_div_list[-1].contents[1].contents[3].contents if
                              dircetor != "\n"])

            return staff_type, staff
        except:
            return "null", "null"
