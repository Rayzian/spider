# -*- codind:utf-8 -*-

import os
import gzip
import json
import time
import datetime
from inSertData import InsertData
from multiprocessing.managers import BaseManager


class TaskWork(object):
    def __init__(self):
        BaseManager.register("put_task_queue")
        server_addr = "127.0.0.1"
        print "Connect to server %s" % server_addr
        self.m = BaseManager(address=(server_addr, 8001), authkey="zhouxiaoxi")
        self.m.connect()
        self.task = self.m.put_task_queue()

        self.insert = InsertData(host='localHost', name='root', password='zhouxiaoxi', database='CNLog')

    def dataSave(self, data):
        self.insert.insertData(data)


class GZipTool(object):
    def __init__(self, bufSize):
        self.bufSize = bufSize
        self.fin = None
        self.fout = None
        self.task = TaskWork()

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
    decompress_path = ""
    task = task_work.task

    while (not task.empty()):
        try:
            path = task.get(True, timeout=5)
            print "get GZFile %s succeed." % path
            file_name = path.strip().split("/")[-1][:-3]
            decompress_path = path[:-3]
            gz.decompress(gzFile=path, dst=decompress_path)

            begin_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            with open(decompress_path, 'r') as text:
                for temp in text:
                    json_object = json.loads(temp, encoding="utf-8")
                    task_work.dataSave(json_object)
            end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            istruncatelog = 1
            if os.path.exists(decompress_path):
                os.remove(decompress_path)
            task_work.insert.myCallProc(begin_time, end_time, istruncatelog)

        except (EOFError, Exception), e:
            print e
            print "end."
            if os.path.exists(decompress_path):
                os.remove(decompress_path)

    # path = r'/home/zhouxiaoxi/cn_log/2017-08-16-10.gz'
    # file_name = path.strip().split("/")[-1][:-3]
    # decompress_path = path[:-3]
    # gz.decompress(gzFile=path, dst=decompress_path)
    #
    # with open(decompress_path, 'r') as text:
    #     for temp in text:
    #         json_object = json.loads(temp, encoding="utf-8")
