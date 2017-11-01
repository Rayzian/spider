# -*- coding: utf-8 -*-

import json
import codecs


def writeDelaer(data, city, brand):
    filename = "%s_delaer" % city
    with codecs.open(filename=filename, mode="a", encoding="utf-8") as f:
            f.write("%s %s \n" % (data["car_id"], "".join(brand)))
            f.write("%s %s %s \n" % (data["name"], data["phoneNumber"], data["local"]))


def writeCarInfo(data):
    with codecs.open(filename="carInfo", mode="a", encoding="utf-8") as f:
        f.write((json.dumps(data, ensure_ascii=False)))
        f.write("\n")