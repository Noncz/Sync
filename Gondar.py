# -*- coding: utf-8 -
#
# This is the main file

import os
import DB
import sys
import Sync
import Watcher
import Queue
import argparse

# The most sync job
MAX_Q_SIZE = 2 ** 16

# Below is the status a file can be

class Gondar(object):
    """
        Gondar is a FileWatcher and FileSynchronizer.
    """
    def __init__(self, src, time, worker, dbd, logpath, rec):
        """
        @param src: the monitor source directory or file
        @type  src: string

        @param time: The total time to monitor the source,
                     when it come to zero, it means forever
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
        self.src = src or os.getcwd()
        self.time = time or 0
        self.worker = worker or 1

        self.dbd = dbd or "/tmp/Gondar/db"
        self.logpath = logpath or "/tmp/Gondar/Gondar.log"
        self.rec = rec or True

        self.workq_maxsize = MAX_Q_SIZE 
        self.workq = Queue.PriorityQueue(self.workq_maxsize)

    def run(self):
        try:
            db = DB.DB(self, self.dbd)
            db.dump()

            watcher = Watcher.Watcher(self, self.src)
            watcher.loop()

            Sync.Sync(self, self.worker, db)
        except KeyboardInterrupt:
            watcher.stop()
            sys.exit(0)


def Parser(): 
    usage = "Gondar is watching you"
    description = "This is monitor and synchronization tool"
    parser = argparse.ArgumentParser(prog="Gondar",
                                     usage=usage,
                                     description=description)

    parser.add_argument('-s', '--sourcedir')
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

    gdr = Gondar(src=option.sourcedir,
                 time=option.time,
                 worker=option.worker,
                 dbd=option.databasedir,
                 logpath=option.log,
                 rec=option.recursive)

    gdr.run()

if __name__ == "__main__":
    main()
