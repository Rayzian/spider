# -*- coding: utf-8 -*-

import codecs


def writeData(data, suite_type):
    file_name = "appstore_" + str(suite_type) + ".txt"
    with codecs.open(filename=file_name, mode="a", encoding="utf-8") as cf:
        string = data["app_corp"] + "\001" + data["app_name"] + "\001" + data["app_type"] + "\001" + data["description"]
        cf.write(string + "\n")
        cf.write(data["url"] + "\n")
        print data
