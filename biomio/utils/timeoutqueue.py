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
        for t in self.queue.keys():
            if t <= ts:
                expired.extend(self.queue[t])
                del self.queue[t]
            else:
                break
        return expired

    def remove(self, item):
        ts_to_remove = None
        for (t, item_list) in self.queue.iteritems():
            if item in item_list:
                item_list.remove(item)
                if not item_list:
                    ts_to_remove = t
                else:
                    self.queue[t] = item_list
                break
        if ts_to_remove:
            del self.queue[ts_to_remove]

    def iteritems(self):
        return self.queue.iteritems()

    def __str__(self):
        s = "\n"
        for item in self.queue.iteritems():
            s.join('%s %s' % item)
        return s

    def first(self):
        if self.queue:
            (timestamp, item_list) = self.queue.itervalues().next()
            return timestamp
        return None
