# -*- coding: utf-8 -
#
# This is the main file

import os
import argparse 

class Gondar(object):
    """
        Gondar is a FileWatcher and FileSynchronizer.
    """
    def __init__(self, src, time=0, worker=1,
                 dbd="/tmp/Gondar", logpath="/tmp/Gondar.log", rec=True):
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

        @param logpath: the path to put logging file
        @type  logpath: string

        @param rec: if monitor recursivly
        @type  rec: boolean
        """
        self.src = src or os.getcwd()
        self.time = time
        self.worker = worker
        self.dbd = dbd
        self.logpath = logpath
        self.rec = rec

    def init_db(self):
        pass

    def init_watcher(self):
        pass


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
    parser.add_argument('-r', '--recursive')
    parser.add_argument('sync')

    return parser


def main():
    parser = Parser()
    option = parser.parse_args()
    print option


if __name__ == "__main__":
    main()
