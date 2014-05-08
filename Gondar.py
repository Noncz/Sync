# -*- coding: utf-8 -
#
# This is the main file

import os
import sys
import heapq
import upyun
import Queue
import leveldb
import argparse

import DB
import Sync
import Watcher

from Util import Task


class Up(object):
    pass

class Gondar(object):
    """
        Gondar is a FileWatcher and FileSynchronizer.
    """
    def __init__(self, src, dst, time, worker, dbd, logpath, rec):
        """
        @param src: the monitor source directory or file
        @type  src: string

        @param time: The total time to monitor the source,
                     when it equals zero, it means forever
        @type  time: integer

        @param worker: The number of multithread
        @type  worker: integer

        @param dbd: the directory to put db file
        @type  dbd: string

        @param db: the database
        @type  db: class DB.DB()

        @param logpath: the path to put logging file
        @type  logpath: string

        @param rec: if monitor recursivly
        @type  rec: boolean

        @param workq: the multi-thread work queue
        @type  workq: Queue.Queue()
        """
        self.src = src
        self.dst = dst
        self.time = time or 0
        self.worker = worker or 1

        self.db = DB.DB(self, dbd or "/tmp/Gondar/db")
        self.logpath = logpath or "/tmp/Gondar/Gondar.log"
        self.rec = rec or True

        self.workq = Queue.PriorityQueue(0)

    def init_src(self):
        """
            Scan the direcory(recursive or not), if the file/filter
            have a unfinished job left(judge by db), then we just use
            that record in db, if not, we create a new record for this
            file/filter, the record is up to Put it to remote.At last,
            dump the db record to workq.
        """
        def scan(rootdir):
            for lists in os.listdir(rootdir):
                path = os.path.join(rootdir, lists)
                if self.rec and os.path.isdir(rootdir):
                    scan(path)
                yield path

        for abspath in scan(self.src):
            value = ""
            tic = lambda : time.time()
            if not self.db.Get(abspath):
                relpath = os.path.relpath(abspath, self.src)
                remotepath = os.path.join(self.dst, relpath)
                if os.path.isdir(abspath):
                    value = "Mkdir %s:%f:%d" % (remotepath, tic(), 10)
                else:
                    value = "Put %s %s:%f:%d" % (abspath, remotepath, tic() + 60, 5)
                self.db.Put(abspath, value)
            self.workq.put(Task(value))

    def run(self):
        self.init_src()
        watcher = Watcher.Watcher(self, self.workq, self.src, self.dst)
        watcher.loop()
        Sync.Start(self, self.worker, db)

def Parser():
    usage = "Gondar is watching you"
    description = "This is monitor and synchronization tool"
    parser = argparse.ArgumentParser(prog="Gondar",
                                     usage=usage,
                                     description=description)

    parser.add_argument('-s', '--sourcedir')
    parser.add_argument('-u', '--uploaddir')
    parser.add_argument('-t', '--time')
    parser.add_argument('-d', '--deamon', action='store_true')
    parser.add_argument('-w', '--worker')
    parser.add_argument('-b', '--databasedir')
    parser.add_argument('-l', '--log')
    parser.add_argument('-r', '--recursive', action='store_true')

    return parser


def main():
    parser = Parser()
    option = parser.parse_args()
    
    if not option.sourcedir or not option.uploaddir:
        parser.print_help()
        sys.exit(0)

    gdr = Gondar(src=option.sourcedir,
                 dst=option.uploaddir,
                 time=option.time,
                 worker=option.worker,
                 dbd=option.databasedir,
                 logpath=option.log,
                 rec=option.recursive)

    gdr.run()

if __name__ == "__main__":
    main()
