# -*- coding: utf-8 -*-

import json
import codecs

def writeDelaer(data, city):
    filename = "%s_delaer" % city
    with codecs.open(filename=filename, mode="a", encoding="utf-8") as f:
            f.write((json.dumps(data, ensure_ascii=False)))
            f.write("\n")


def writeCarInfo(data):
    with codecs.open(filename="carInfo", mode="a", encoding="utf-8") as f:
        f.write((json.dumps(data, ensure_ascii=False)))
        f.write("\n")