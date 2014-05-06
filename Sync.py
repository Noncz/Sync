# -*- coding: utf-8 -

import pdb
import threading
import logging

import DB

def Sync(gdr, w, db):
    for i in range(w):
        Worker(gdr, db).start()

class Worker(threading.Thread):
    def __init__(self, gdr, db):
        self.workq = gdr.workq
        self.db = db
        threading.Thread.__init__(self)

    def run(self):
        while True:
            item = self.workq.get()
            self.upload(item)
            self.db.Put(item, DB.FILE_STATUS_SYNCED)

    def upload(src):
        pass
