# -*- coding: utf-8 -*-

import time
import codecs


def writeData(data, operator):
    local_time = time.strftime("%Y%m%d", time.localtime(time.time()))
    file_name = "WeiXin_" + local_time + "_" + operator + "_.txt"
    with codecs.open(filename=file_name, mode="a", encoding="utf-8") as wf:
        string = data["time"] + "\001" + data["public"] + "\001" + data["title"] + "\001" + data["contents"] + "\001" + \
                 data["url"]
        wf.write(string)
        wf.write("\n")
