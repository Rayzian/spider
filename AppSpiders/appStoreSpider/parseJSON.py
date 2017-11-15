# -*- coding: utf-8 -*-

import json
from bs4 import BeautifulSoup
from getJSON import downloader
from dataOut import writeData


class Paser(object):
    def json_parser(self, url, suite_type):
        web_data = downloader(url)
        if web_data:
            json_value = json.loads(web_data)["results"]
            for value in json_value:
                data = {
                    "description": self._get_description(json_value[value]["url"]),
                    "app_name": json_value[value]["name"],
                    "app_type": " ".join(json_value[value]["genreNames"]),
                    "app_corp": json_value[value]["artistName"],
                    "url": json_value[value]["url"]
                }

                writeData(data, suite_type)

    def _get_description(self, url):
        data = downloader(url, is_headers=False)

        if data:
            soup = BeautifulSoup(markup=data, features="lxml")
            desc = soup.find(name="p", attrs={"itemprop": "description"})
            return desc.text
