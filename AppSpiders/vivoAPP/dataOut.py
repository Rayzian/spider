# -*- coding: utf-8 -*-

import codecs


def writeData(data, rank_name):
    file_name = "vivo" + rank_name + ".txt"
    with codecs.open(filename=file_name, mode="a", encoding="utf-8") as cf:
        cf.write("%s\001%s\001%s\001%s\001%s\n" % (
            data["rank"], data["name"], data["tag"], data["developer"], data["introduction"]))
        print data
