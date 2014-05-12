# -*- coding: utf-8 -

import time
import upyun
import Queue
import threading
import logging

import DB
import config

workl = []

def Start(gdr, w, db):
    up = upyun.UpYun(config.bucket,
                     config.user,
                     config.passwd)
    try:
        up.getlist()
    except:
        raise

    for i in range(w):
        workl.append(Worker(gdr, db, up))

    for worker in workl:
        worker.start()

    gdr.workq.join()

def Stop():
    for worker in workl:
        worker.alive = False

class Worker(threading.Thread):
    def __init__(self, gdr, db, up):
        threading.Thread.__init__(self)
        self.workq = gdr.workq
        self.db = db
        self.up = up
        self.alive = True

    def run(self):
        while self.alive:
            try:
                task = self.workq.get_nowait()
            except Queue.Empty:
                task = None

            if not task:
                time.sleep(0.1)
                continue

            self.handle(task)
            self.workq.task_done()
    
    def handle(self, task):
        now = time.time()
        if task.delay > now:
            time.sleep(task.delay - now)

        cmd = task.cmd.split(" ")

        try:
            if cmd[0] == "Put":
                with open(cmd[1]) as f:
                    self.up.put(cmd[2], f)
            elif cmd[0] == "Mkdir":
                up.mkdir(cmd[1])
            elif cmd[0] == "Delete":
                up.delete(cmd[1])
        except:
            raise
        else:
            self.db.Delete(task.path)

    def stop(self):
        self.stop = False
