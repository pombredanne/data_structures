#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
try:
    import bitarray
except:
    raise ImportError('ApproximateCounter requires bitarray >= 0.8.1')

import random


__date__ = '17 Jan 2015'
__author__ = 'Paul Tune'

# use this function to check if all bits are set to 1
def check_bits(b, n):
    mask = (1 << n) - 1
    yield (b & mask) == mask

class ApproximateCounter:
    def __init__(self, num_counters=1, counter_size=8):
        self.num_counters = num_counters
        self.counters = [0] * self.num_counters
        # initialize counters
        self.counters = []
        for _ in range(num_counters):
            self.counters.append(bitarray(2**counter_size))

    def update(self, item):
        # flip the count equal to the count of the counter
        for _ in range(self.counters[item]):
            if not random.randint(0,1):
                return

        self.counters[item] +=1

    def query(self, item):
        return self.counters[item]

    def __len__(self):
        return self.num_counters


if __name__ == "__main__":
    test = [1] * 1000

    approx_counter = ApproximateCounter()
    for item in test:
        approx_counter.update(item-1)

    print(approx_counter.query(0))
