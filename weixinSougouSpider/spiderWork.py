# -*- coding: utf-8 -*-

import codecs
from weixinSougouSpider.paserClass import Paser


# def start_work(url):

if __name__ == '__main__':

    parser = Paser()

    url = "http://weixin.sogou.com/weixin?type=1&s_from=input&query="

    start_url_dict = {
        "yidong": r'/Users/zhouxiaoxi/Desktop/yidong.txt',
        "dianxin": r'/Users/zhouxiaoxi/Desktop/dianxin.txt',
        "liantong": r'/Users/zhouxiaoxi/Desktop/liantong.txt'
    }

    for operator in start_url_dict.keys():
        with codecs.open(filename=start_url_dict[operator], mode="r", encoding="utf-8") as f:
            for query in f:
                query_url = url + query.strip().split("|")[-1]
                parser.parse_links(url=query_url, operator=operator)