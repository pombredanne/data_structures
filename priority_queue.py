from heapq import heapify, heappop, heappush

__author__ = 'Paul Tune'
__date__ = '22 Jan 2016'

class PriorityQueueSet(object):
    """
    Combined priority queue and set data structure. Acts like a priority queue, except that its items are guaranteed to
    be unique.

    Provides O(1) membership test, O(log N) insertion and O(log N) removal of the smallest item.

    Modified code from Eli Bendersky. See http://stackoverflow.com/questions/407734/a-generic-priority-queue-for-python

    Important: the items of this data structure must be both comparable and hashable (i.e. must implement __cmp__ and
    __hash__). This is true of Python's built-in objects, but you should implement those methods if you want to use
    the data structure for custom objects.
    """
    def __init__(self, items=[]):
        """
        Create a new PriorityQueueSet.

        :param items: initial item list - it can be unsorted and non-unique. The data structure will be created in O(N).
        """
        # set stores the item, its priority and its membership
        self.set = dict((item, True) for item in items)
        self.heap = self.set.keys()
        heapify(self.heap)

    def has_item(self, item):
        """
        Check if item exists in the queue

        :param item: queried item
        """
        return item in self.set

    def pop_minimum(self):
        """
        Remove and return the smallest item from the queue
        """
        smallest = heappop(self.heap)
        del self.set[smallest]
        return smallest

    def add(self, item):
        """
        Add item to the queue. The item will be added only if it doesn't already exist in the queue.

        :param item: item to add
        """
        if not (item in self.set):
            self.set[item] = True
            heappush(self.heap, item)

    def change_priority(self, item):
        """
        Change the priority of the item

        :param item: item's priority to change
        """
        return

