# -*- coding: utf-8 -*-

import time
import threading
import Queue
import paramiko
from multiprocessing.managers import BaseManager

class taskServerTest(object):

    def __init__(self):
        self.task_queue = Queue.Queue()
        self.result_queue = Queue.Queue()


    def Serverstart(self):
        BaseManager.register("put_task_queue", callable=lambda: self.task_queue)
        BaseManager.register("get_result_queue", callable=lambda: self.result_queue)

        self.manager = BaseManager(address=("", 8001), authkey="zhouxiaoxi")

        self.manager.start()

        return self.manager


    def sendSSHCmd(self, hostname, filepath, port=22, username="zhouxiaoxi",
                   password="1"):
        ssh = paramiko.SSHClient()

        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, port=port, username=username, password=password)

        cmd = "python {}".format(filepath)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        result = stdout.read()
        if not result:
            result = stderr.read()
        ssh.close()

        print result.decode()

    def queueClose(self):
        self.manager.shutdown()

if __name__ == '__main__':

    server = taskServerTest()
    manager = server.Serverstart()
    task = manager.put_task_queue()
    print task
    result = manager.get_result_queue()

    server_thd = threading.Thread(target=server.sendSSHCmd, args=("192.168.164.131",
                                                                  "/home/zhouxiaoxi/taskwork.py"))
    # server.sendSSHCmd(hostname="192.168.164.131",
    #                    filepath="/home/zhouxiaoxi/taskwork.py")

    server_thd.start()
    time.sleep(5)

    print "try get result"
    while True:
        if task.empty():
            break
        result = task.get(timeout=15)
        print "result is {}".format(result)
        time.sleep(15)

    print "shutdown the queue."
    server.queueClose()