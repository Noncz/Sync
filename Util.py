class Task(object):
    """
        The item in Priority Queue
    """
    def __init__(self, value):
        cmd, delay, pri = value.split(":")
        self.cmd = cmd
        self.delay = float(delay)
        self.pri  = int(pri)

    def __lt__(self, other):
        if self.pri > other.pri:
            return True
        elif self.pri == other.pri:
            return self.delay < other.delay
        else:
            return False
