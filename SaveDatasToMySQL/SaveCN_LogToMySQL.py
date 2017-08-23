# -*- coding: utf-8 -*-

import gzip
import zipfile
import shutil
import os
import datetime
import time
import Queue
from multiprocessing.managers import BaseManager


class TaskServer(object):
    def __init__(self):
        self.file_queue = Queue.Queue()


    def startServer(self):
        BaseManager.register("put_file_queue", callable=lambda: self.file_queue)

        self.manager = BaseManager(address=("", 8001), authkey="zhouxiaoxi")
        self.manager.start()

        return self.manager

    def getLogFile(self, file_path):
        for path, dir, file in os.walk(file_path):
            print "dir :", path
            # print "path :", path
            print "file :", file
            gzfile_list = [path + "/" + i for i in file]
            print "gzfile_list : ", gzfile_list
            print "-" * 45
            return gzfile_list

class GZipTool(object):
    def __init__(self, bufSize):
        self.bufSize = bufSize
        self.fin = None
        self.fout = None

    def compress(self, src, dst):
        self.fin = open(src, 'rb')
        self.fout = gzip.open(dst, 'wb')

        self.__in2out()

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
    file_path = raw_input("file_path: ")
    buffer_size = raw_input("buffer_size: ")

    server = TaskServer()
    decompress = GZipTool(bufSize=int(buffer_size))

    gzfile_list = server.getLogFile(file_path=file_path)
    for gzfile in gzfile_list:
        file_name = gzfile.strip().split("/")[-1][:-3]
        decompress.decompress(gzFile=gzfile, dst=(file_path + '/' +file_name))