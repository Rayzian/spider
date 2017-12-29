# -*- coding: utf-8 -*-

from parserJSON import Parser

if __name__ == '__main__':

    p = Parser()

    rank_name = [u'网游榜']
    for name in rank_name:
        p.get_app_rank(rank_name=name)
