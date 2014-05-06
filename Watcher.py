# -*- coding: utf-8 -
#
# This is the monitor module using pyinotify

from pyinotify import ProcessEvent, WatchManager, ThreadedNotifier, IN_CREATE


class WatcherException(Exception):
    pass


class EventHandler(ProcessEvent):
    def __init__(self, workq):
        self.workq = workq

    def process_IN_CREATE(self, event):
        self.workq.put(event.pathname)


class Watcher(object):
    """
        Watching on the fly
    """
    def __init__(self, gdr, src):
        self.gdr = gdr
        self.src = src

    def loop(self):
        wm = WatchManager()
        mask = IN_CREATE
        wm.add_watch(self.src, mask, rec=self.gdr.rec)
        self.notifier = ThreadedNotifier(wm, EventHandler(self.gdr.workq))
        self.notifier.start()

    def stop(self):
        self.notifier.stop()
