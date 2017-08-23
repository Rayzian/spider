# -*- coding: utf-8 -*-

import os
import json
import gzip
import datetime


def demo(file_path):
    print "-" * 45
    print "Enter demo"
    print "begin: ", datetime.datetime.now()
    for dir, path, file in os.walk(file_path):
        print "dir :", dir
        # print "path :", path
        print "file :", file
        print "end: ", datetime.datetime.now()
        print "-" * 45
        return file




# def zipFile(file_name, file_path):
#     print "-" * 45
#     print "Enter zipFile"
#     print datetime.datetime.now()
#     json_name = file_name.replace(".gz", ".json")
#     json_path = os.path.join(file_path, json_name)
#     gz_path = os.path.join(file_path, file_name)
#     gz = gzip.GzipFile(fileobj=open(gz_path, mode="wb"), mode="rb", compresslevel=9)
#     open(json_path, "wb").write(gz.read())
#     print datetime.datetime.now()
#     print "-" * 45


class GZipTool(object):
    def __init__(self, bufSize):
        self.bufSize = bufSize
        self.fin = None
        self.fout = None


    def decompress(self, gzFile, dst):
        self.fin = gzip.open(gzFile, 'rb')
        self.fout = open(dst, 'wb')

        self.__in2out()

    def __in2out(self, ):
        while True:
            buf = self.fin.read(self.bufSize)
            if len(buf) < 1:
                break
            self.fout.write(buf)

        self.fin.close()
        self.fout.close()

if __name__ == '__main__':

    file_path = r'D:\SQL&LOG\cn_log'

    file_list = demo(file_path)

    # for i in file_list:
    # zipFile(file_name=file_list[2], file_path=file_path)
    file_name = file_list[3]
    gz_path = os.path.join(file_path, file_name)
    json_name = file_name.replace(".gz", ".json")
    json_path = os.path.join(file_path, r'2017-08-11-03')
    print "-" * 45
    print "decompress"
    print datetime.datetime.now()
    gz = GZipTool(bufSize=1024*8)
    gz.decompress(gzFile=gz_path, dst=json_path)
    print datetime.datetime.now()
    print "-" * 45
    print "reading file..."
    print datetime.datetime.now()
    with open(json_path, 'r') as text:
        for temp in text:
            json_object = json.loads(temp, encoding="utf-8")
            print temp
    print datetime.datetime.now()
    print "read ended."


