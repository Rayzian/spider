# -*- coding: utf-8 -*-

import codecs
import json

def writeData(data, plat, type):
    file_name = "%s_%s_rank" % (plat, type)
    with codecs.open(filename=file_name, mode="a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False))
        f.write("\n")