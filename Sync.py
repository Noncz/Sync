# -*- coding: utf-8 -

import time
import upyun
import threading
import logging

import DB

def Start(gdr, w, db):
    for i in range(w):
        Worker(gdr, db).start()

    gdr.workq.join()

class Worker(threading.Thread):
    def __init__(self, gdr, db):
        threading.Thread.__init__(self)
        self.workq = gdr.workq
        self.db = db

    def run(self):
        while True:
            task = self.workq.get()
            self.handle(task)
            self.workq.task_done()
    
    def handle(self, task):
        now = time.time()
        if task.delay > tic():
            time.sleep(now - task.delay)

        cmd = task.cmd.split("")

        if cmd[0] == "Put":
            pass
        elif cmd[0] == "Mkdir":
            pass
