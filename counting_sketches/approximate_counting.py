try:
    import bitarray
except:
    raise ImportError('ApproximateCounter requires bitarray >= 0.8.1')

import random


__date__ = '17 Jan 2015'
__author__ = 'Paul Tune'


class ApproximateCounter:
    def __init__(self, num_counters=1, counter_size=8):
        self.counters = []

        for _ in range(num_counters):
            self.counters.append(bitarray(2**counter_size))

    def update(self, id):
        # flip the count equal to the count of the counter
        for _ in range(self.counters[id]):
            coin = random.getrandbits(self.counters[id])

            if :
                self.counters[id] +=1
