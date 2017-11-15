# -*- coding: utf-8 -*-

import redis


class MyRedis(object):
    def __init__(self):
        self.conn = redis.Redis(host="localHost", port=6379)

    def save_urls(self, db, q, additional=False, new=False):
        if additional:
            while (not q.empty()):
                url = q.get(timeout=1)
                self.conn.sadd(db, url)
        else:
            result = self.check_urls_number(db)
            if result and not new:
                print "There are %s urls in redis-queue." % str(result)
            elif result and new:
                print "There are %s urls in redis-queue." % str(result)
                self.save_urls(db, q, additional=True)


    def get_urls(self, db, num):
        result = self.check_urls_number(db)
        if result:
            url_list = []
            for i in xrange(num):
                url_list.append(self.conn.spop(db))

            if url_list:
                return url_list
            return None
        else:
            print "None urls be getted."
            return

    def check_urls_number(self, db):
        result = len(self.conn.smembers(db))

        if result != 0:
            return result
        else:
            return False
