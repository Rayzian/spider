# -*- coding:utf-8 -*-

import time
from multiprocessing.managers import BaseManager

class TaskWork(object):

    def __init__(self):

        BaseManager.register("put_task_queue")

        server_add = "192.168.164.129"

        print "Connect server {}...".format(server_add)

        self.conn = BaseManager(address=(server_add, 8001), authkey="zhouxiaoxi")
        self.conn.connect()

        print "__init__ end. "

    def putData(self):
        put_tast = self.conn.put_task_queue()
        for i in xrange(100):
            put_tast.put(str(i))
            time.sleep(10)



if __name__ == '__main__':
    m = TaskWork()
    m.putData()
