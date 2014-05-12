# -*- coding: utf-8 -
#
# This is the monitor module using pyinotify

import os
import time
from pyinotify import ProcessEvent, WatchManager, \
    ThreadedNotifier, IN_CREATE, IN_MODIFY
from Util import Task

tic = lambda : time.time()

class WatcherException(Exception):
    pass


class EventHandler(ProcessEvent):
    def __init__(self, workq, src, dst):
        self.workq = workq
        self.src = src
        self.dst = dst

    def process_IN_CREATE(self, event):
        path = event.pathname
        remotepath = self.getremotepath(path)

        value = "Put %s %s:%f:%d" % (path, remotepath, tic() + 60, 5)
        self.addtoqueue(path, value)

    def process_IN_DELETE(self, event):
        path = event.pathname
        remotepath = self.getremotepath(path)

        value = "Delete %s:%f:%d" % (path, remotepath, tic() + 10, 5)
        self.addtoqueue(path, value)

    def process_IN_MODIFY(self, event):
        self.process_IN_CREATE(event)

    def getremotepath(self, path):
        relpath = os.path.relpath(path, self.src)

    def addtoqueue(self, path, value):
        self.workq.put(Task(path, value))
        self.gdr.db.Put(path, value)


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
        handler = EventHandler(self.workq, self.src, self.dst)

        self.notifier = ThreadedNotifier(wm, handler)
        self.notifier.start()

        mask =  IN_CREATE | IN_MODIFY
        wm.add_watch(self.src, mask, rec=self.gdr.rec)

    def stop(self):
        self.notifier.stop()
