# -*- coding: utf-8 -*-

import os
import sys
import time
import Queue
import subprocess
from multiprocessing.managers import BaseManager, Process


class TaskServer(object):
    def __init__(self):
        self.task_queue = Queue.Queue()

    def Serverstart(self):
        BaseManager.register("put_task_queue", callable=lambda: self.task_queue)

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

    def startWorkServer(self):
        current_path = sys.path[0]
        cmd = "python {}/workServer.py".format(current_path)
        # subprocess.Popen(cmd.split(" "))
        os.system(cmd)

    def queueClose(self):
        self.manager.shutdown()


if __name__ == '__main__':

    folder_path = raw_input("Please enter the path of the log folder: ")

    server = TaskServer()
    manager = server.Serverstart()
    task = manager.put_task_queue()

    gzfile_list = server.getLogFile(file_path=folder_path)
    workserver_proc = Process(target=server.startWorkServer)
    workserver_proc.start()

    map(lambda x: task.put(x), gzfile_list)
    # for i in range(5):
    #     server.startWorkServer()

    # manager.get_server().serve_forever()

    # if not task.empty():
    #     for i in range(5):
    #
    # else:
    #     time.sleep(1)
    #     for i in range(5):
    #         server.startWorkServer()

    while True:
        if task.empty():
            break
    server.queueClose()
