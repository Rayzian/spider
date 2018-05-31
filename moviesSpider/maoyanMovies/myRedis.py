# -*- coding: utf-8 -*-


import redis


class MyRedis(object):
    def __init__(self, db, additional=False, new=False):
        self.db = db
        self.conn = redis.Redis(host="localhost", port=6379)
        if new:
            self._delete_redis_queue()
        self.additional = additional

    def save_urls(self, movie_url):

        if self.additional:
            print "save %s " % movie_url
            self.conn.sadd(self.db, movie_url)
        else:
            result = self.check_urls_number()
            if result:
                print "There are %s urls in redis-queue." % str(result)

    def get_urls(self):

        result = self.check_urls_number()
        if result:
            return self.conn.spop(self.db)
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
