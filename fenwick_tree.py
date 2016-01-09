from math import log, ceil


__author__ = 'Paul Tune'


class FenwickTree:
    def __init__(self, arr):
        self.maxval = len(arr)
        # insert into Fenwick Tree
        self.tree = [0] * self.maxval
        # index 0 is special: we don't use it
        for i in range(1, self.maxval):
            # print('Inserting item %d' % i)
            self.add_value(i, arr[i])

    def get_cumulative_sum(self, index):
        cumsum = 0
        while index > 0:
            cumsum += self.tree[index]
            # this finds the last non-zero bit each time
            index -= index & -index

        return cumsum

    def get(self, index):
        return self.get_cumulative_sum(index) - self.get_cumulative_sum(index-1)

    def add_value(self, index, value):
        while index < self.maxval:
            self.tree[index] += value
            index += index & -index

    def scale(self, c):
        for i in range(self.maxval):
            self.tree[i] /= float(c)

    def find(self, cumsum):
        index = 0
        # start with the most significant bit
        shift = int(ceil(log(self.maxval,2)))
        bit_mask = 1
        bit_mask <<= shift-1

        # binary search style
        while (bit_mask != 0 and index < self.maxval):
            test_index = index + bit_mask
            if (cumsum >= self.tree[test_index]):
                index = test_index
                cumsum -= self.tree[index]

            # update bit mask
            bit_mask >>= 1

        if cumsum != 0:
            return -1

        return index

if __name__ == '__main__':
    print('Test Fenwick Tree:')
    a = [0, 4, -2, 8, 5, 1, 9, 6, 3, 5, 8, 6, 6, -3, 5, 2]

    fenwick_tree = FenwickTree(a)

    print('Cumulative sum')
    print('get_cumulative_sum(1): %d' % fenwick_tree.get_cumulative_sum(1))
    print('get_cumulative_sum(3): %d' % fenwick_tree.get_cumulative_sum(3))
    print('get_cumulative_sum(5): %d' % fenwick_tree.get_cumulative_sum(5))
    print('get_cumulative_sum(9): %d' % fenwick_tree.get_cumulative_sum(9))
    print('get_cumulative_sum(15): %d' % fenwick_tree.get_cumulative_sum(15))

    print
    print('Single item')
    print('get(5): %d' % fenwick_tree.get(5))

    print
    print('Add value')
    fenwick_tree.add_value(5, 4)
    print('add_value(5, 4): %d' % fenwick_tree.get(5))

    print
    print('Find')
    print('find(10): %d' % fenwick_tree.find(10))

    print
    print('Scale by 3')
    fenwick_tree.scale(3)
    print('get(5): %f' % fenwick_tree.get(5))

