
from collections import OrderedDict

class TimeoutQueue:
    def __init__(self):
        self.queue = OrderedDict()

    def __nonzero__(self):
        return bool(self.queue)

    def create_timeout(self, ts):
        self.queue[ts] = []

    def has_ts(self, ts):
        return ts in self.queue

    def append(self, ts, item):
        self.queue[ts].append(item)

    def has_expired(self, ts):
        (timestamp, item_list) = self.queue.itervalues().next()
        return timestamp < ts

    def take_expired(self, ts):
        expired = []
        expired_ts = []
        for (t, item_list) in self.queue.iteritems():
            if t <= ts:
                expired.extend(item_list)
                expired_ts.append(t)
            else:
                break

        for t in expired_ts:
            del self.queue[t]

        return expired

    def remove(self, item):
        ts_to_remove = None
        for (t, item_list) in self.queue.iteritems():
            if item in item_list:
                item_list.remove(item)
                if not item_list:
                    ts_to_remove = t
                break
        if ts_to_remove:
            del self.queue[ts_to_remove]

    def iteritems(self):
        return self.queue.iteritems()

    def __str__(self):
        s = ''
        for (t, item_list) in self.queue.iteritems():
            s += '%s  %s\n' % (str(t), str(item_list))
        return s
