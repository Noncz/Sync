# -*- coding: utf-8 -
#
# This is the monitor module using pyinotify

import os
import time
from pyinotify import ProcessEvent, WatchManager, 
    ThreadedNotifier, IN_CREATE
from Util import Task


class WatcherException(Exception):
    pass


class EventHandler(ProcessEvent):
    tic = lambda : time.time()
    def __init__(self, workq, src, dst):
        self.workq = workq
        self.src = src
        self.dst = dst

    def process_IN_CREATE(self, event):
        path = event.pathname
        remotepath = GetRemotePath(path)

        value = "Put %s %s:%f:%d" % (path, remotepath, tic() + 60, 5)
        self.workq.put(Task(value))

    def GetRemotePath(self, path):
        relpath = os.path.relpath(path, self.src)


class Watcher(object):
    """
        Watching on the fly
    """
    def __init__(self, gdr, workq, src, dst):
        self.gdr = gdr
        self.workq = workq 
        self.src = src
        self.dst = dst

    def loop(self):
        wm = WatchManager()
        mask = IN_CREATE
        wm.add_watch(self.src, mask, rec=self.gdr.rec)
        self.notifier = ThreadedNotifier(wm, 
                            EventHandler(self.workq, self.src, self.dst))
        self.notifier.start()

    def stop(self):
        self.notifier.stop()
