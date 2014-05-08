# -*- coding: utf-8 -

import os
import leveldb

class DB(object):
    """
        The persistant part, write down the current work status
    """

    def __init__(self, gdr, dbd, workq):
        """
        @param gdr: the gondar object
        @type  gdr: class Gondar

        @param dbd: the DataBase Directiry
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
