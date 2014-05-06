# -*- coding: utf-8 -

import os
import pdb
import leveldb

FILE_STATUS_SYNCED = "1"
FILE_STATUS_TOSYNC = "2"

class DB(object):
    """
        The persistant part, write down the current work status
    """

    def __init__(self, gdr, dbd):
        """
        @param gdr: the gondar object
        @type  gdr: class Gondar

        @param dbd: the DataBaseDirectiry
        @type  dbd: string
        """
        self.gdr = gdr
        self.db = leveldb.LevelDB(dbd)

    def Get(self, key):
        try:
            return self.db.Get(key)
        except KeyError:
            return None

    def Put(self, key, value):
        self.db.Put(key, value)

    def dump(self):
        src = self.gdr.src
        workq = self.gdr.workq

        if not os.path.isdir(src):
            if not self.Get(src):
                self.Put(src, FILE_STATUS_TOSYNC)
                workq.put(src)
        else:
            for root, dirs, files in os.walk(src):
                for d in dirs:
                    path = os.path.join(root, d)
                    status = self.Get(path)
                    if status is not FILE_STATUS_SYNCED:
                        if not status:
                            self.Put(path, FILE_STATUS_TOSYNC)
                        workq.put(path)
                for f in files:
                    path = os.path.join(root, f)
                    status = self.Get(path)
                    if status is not FILE_STATUS_SYNCED:
                        if not status:
                            self.Put(path, FILE_STATUS_TOSYNC)
                        workq.put(path)

    def clear(self):
        pass
