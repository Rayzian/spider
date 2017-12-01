# -*- coding: utf-8 -*-

import json
import codecs


def writeDelaer(data, city, brand):
    filename = "%s_delaer" % city
    with codecs.open(filename=filename, mode="a", encoding="utf-8") as f:
            f.write("%s\001%s\001%s\001%s\001%s\n" % (data["car_id"], "".join(brand[1:]), data["name"], data["phoneNumber"], data["local"]))
            # f.write("%s\001%s\001%s \n" % (data["name"], data["phoneNumber"], data["local"]))


def writeCarInfo(data):
    with codecs.open(filename="carInfo", mode="a", encoding="utf-8") as f:
        f.write((json.dumps(data, ensure_ascii=False)))
        f.write("\n")