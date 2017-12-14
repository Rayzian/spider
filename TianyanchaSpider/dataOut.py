# -*- coding: utf-8  -*-

import codecs


def writeData(data):
    file_name = "channel_cp.txt"
    with codecs.open(filename=file_name, mode="a", encoding="utf-8") as cf:
        if len(data.keys()) == 9:
            cf.write("%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (
                data["company_name"], data["organizing_code"], data["credit_code"], "-".join(data["person"]),
                "-".join(data["position"]), data["person_count"], "-".join(data["holder"]),
                "-".join(data["holder_prop"]), data["legal_person"]))

        elif len(data.keys()) < 9:
            if ("person" in data) and ("holder" not in data):
                cf.write("%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (
                    data["company_name"], data["organizing_code"], data["credit_code"], "-".join(data["person"]),
                    "-".join(data["position"]), data["person_count"], " ", " ", data["legal_person"]))

            elif ("person" not in data) and ("holder" in data):
                cf.write("%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (
                    data["company_name"], data["organizing_code"], data["credit_code"], " ", " ", " ",
                    "-".join(data["holder"]),
                    "-".join(data["holder_prop"]), data["legal_person"]))

            elif ("person" not in data) and ("holder" not in data):
                cf.write("%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (
                    data["company_name"], data["organizing_code"], data["credit_code"], " ", " ", " ", " ", " ",
                    data["legal_person"]))
