# -*- coding: utf-8 -*-

import os
import codecs


def writeData(data, date, operator):
    floder_path = r"/data/yuqing/weixin"
    file_name = "WeiXin_info_%s_%s.txt" % (date, operator)

    target_file = os.path.join(floder_path, file_name)

    with codecs.open(filename=target_file, mode="a", encoding="utf-8") as cf:
        cf.write("%s\001%s\001%s\001%s\001%s\001%s\001%s\001%s\n" % (
            data["time"], data["name"], data["title"], data["content"], data["reprint"], data["comment"],
            data["public_like"], data["public_read"]))
