# -*- coding: utf-8 -*-

import codecs
import os


class DataWrite(object):
    def __init__(self):
        if not os.path.exists("spiderfilm_HotOnlineMovies_info.txt"):
            with codecs.open(filename="spiderfilm_HotOnlineMovies_info.txt", encoding="utf-8", mode="a") as cf:
                cf.write(
                    "%s\001%s\001%s\001%s\001%s\001%s\001%s\n" % (u'网站', u'影片编号', u"影片名称", u"地区", u"演员名称", u"导演",
                                                                  u"类型"))

    def write(self, data):
        with codecs.open(filename="spiderfilm_HotOnlineMovies_info.txt", encoding="utf8", mode="a") as cf:
            cf.write("%s\001%s\001%s\001%s\001%s\001%s\001%s\n" % (
                data["web"], data["movieID"], data["name"], data["local"], data["actor"], data["director"],
                data["movie_type"]))
