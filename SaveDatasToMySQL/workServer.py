# -*- codind:utf-8 -*-

import gzip
import json
import time
import datetime
from multiprocessing.managers import BaseManager


class TaskWork(object):
    def __init__(self):
        BaseManager.register("put_task_queue")
        server_addr = "127.0.0.1"
        print "Connect to server %s" % server_addr
        self.m = BaseManager(address=(server_addr, 8001), authkey="zhouxiaoxi")
        self.m.connect()
        self.task = self.m.put_task_queue()


class GZipTool(object):
    def __init__(self, bufSize):
        self.bufSize = bufSize
        self.fin = None
        self.fout = None

    def decompress(self, gzFile, dst):
        print "-" * 45
        print "start to decompress :", gzFile
        print datetime.datetime.now()
        self.fin = gzip.open(gzFile, 'rb')
        self.fout = open(dst, 'wb')
        self.__in2out()
        print "decompress {} final.".format(gzFile)
        print datetime.datetime.now()
        print "-" * 45

    def __in2out(self, ):
        while True:
            buf = self.fin.read(self.bufSize)
            if len(buf) < 1:
                break
            self.fout.write(buf)
        self.fin.close()
        self.fout.close()


if __name__ == '__main__':
    task_work = TaskWork()
    gz = GZipTool(bufSize=8192)

    task = task_work.task
    try:
        while (not task.empty()):
            path = task.get(True, timeout=5)
            print "get GZFile succeed %s" % path
            file_name = path.strip().split("/")[-1][:-3]
            dst = path + '/' + file_name
            gz.decompress(gzFile=path, dst=dst)

            with open(dst, 'r') as text:
                for temp in text:
                    json_object = json.loads(temp, encoding="utf-8")

                    # TODO
                    # MySQL

    except EOFError:
        print "end."
