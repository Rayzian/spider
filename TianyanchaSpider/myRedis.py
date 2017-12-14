# -*- coding: utf-8 -*-

import redis


class MyRedis(object):
    def __init__(self, db, additional=False, new=False):
        self.db = db
        self.conn = redis.Redis(host="localHost", port=6379)
        if new:
            self._delete_redis_queue()
        self.additional = additional

    def save_urls(self, company_name):
        if self.additional:
            print "save %s " % company_name
            self.conn.sadd(self.db, company_name)
        else:
            result = self.check_urls_number()
            if result:
                print "There are %s urls in redis-queue." % str(result)

    def get_urls(self):
        url_list = []
        result = self.check_urls_number()
        if result:
            url_list.append(self.conn.spop(self.db))
            return url_list
        else:
            print "None urls be getted."
            return

    def check_urls_number(self):
        result = self.conn.smembers(self.db)

        if len(list(result)) != 0:
            return True
        else:
            return False

    def _delete_redis_queue(self):
        self.conn.delete(self.db)
