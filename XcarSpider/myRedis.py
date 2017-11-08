# -*- coding: utf-8 -*-

import redis


class MyRedis(object):
    def __init__(self, db, additional=False, new=False):
        self.db = db
        self.conn = redis.Redis(host="localHost", port=6379)
        if new:
            self._delete_redis_queue()
        self.additional = additional

    def save_urls(self, car_info_dict):
        if self.additional:
            print "save %s " % car_info_dict
            self.conn.lpush(self.db, car_info_dict)
        else:
            result = self.check_urls_number()
            if result:
                print "There are %s urls in redis-queue." % str(result)

    def get_urls(self, num):
        result = self.check_urls_number()
        if result:
            url_list = []
            for i in xrange(num):
                url_list.append(self.conn.lpop(self.db))

            if url_list:
                return url_list
            return None
        else:
            print "None urls be getted."
            return

    def check_urls_number(self):
        result = self.conn.llen(self.db)

        if int(result) != 0:
            return True
        else:
            return False

    def _delete_redis_queue(self):
        self.conn.delete(self.db)
