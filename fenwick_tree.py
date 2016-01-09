from math import log, ceil


__author__ = 'Paul Tune'


class FenwickTree:
    '''
    FenwickTree: Fenwick tree data structure, also known as a Binary Indexed Tree.
    Designed for queries of cumulative sums of a set of counts.
    '''
    def __init__(self, arr):
        self.maxval = len(arr) + 1
        # initialise
        self.tree = [0] * self.maxval
        # index 0 is special: we don't use it
        # we thus augment our tree by an additional entry
        for i in range(1, self.maxval):
            self.add_value(i, arr[i-1])

    def get_cumulative_sum(self, index):
        '''
        Computes the cumulative sum from 0 to specified index

        :param index: range from 0 to index
        :return: cumsum: cumulative sum up to index
        '''
        cumsum = 0
        while index > 0:
            cumsum += self.tree[index]
            # this finds the last non-zero bit each time
            index -= index & -index

        return cumsum

    def get(self, index):
        '''
        Returns value of a single item at index

        :param index: location of item
        :return: count of item
        '''
        return self.get_cumulative_sum(index) - self.get_cumulative_sum(index-1)

    def add_value(self, index, value):
        '''
        Insert value at specified index

        :param index: location to update
        :param value: the value to add to location
        '''
        while index < self.maxval:
            self.tree[index] += value
            index += index & -index

    def scale(self, c):
        '''
        Scale counts in Fenwick tree by factor c

        :param c: factor
        '''
        for i in range(1, self.maxval):
            self.tree[i] /= float(c)

    def find(self, cumsum):
        '''
        Find the largest range where the cumulative sum is as
        specified by the parameter. Works if all cumulative sums
        are non-negative.

        :param cumsum: cumulative sum to find
        :return: index where cumulative sum is found
        '''
        index = 0
        # start with the most significant bit
        shift = int(ceil(log(self.maxval, 2)))
        bit_mask = 1
        bit_mask <<= shift-1

        # binary search style
        while bit_mask != 0 and index < self.maxval:
            test_index = index + bit_mask
            if cumsum >= self.tree[test_index]:
                index = test_index
                cumsum -= self.tree[index]

            # update bit mask
            bit_mask >>= 1

        if cumsum != 0:
            return -1

        return index

if __name__ == '__main__':
    print('Test Fenwick Tree:')
    a = [4, -2, 8, 5, 1, 9, 6, 3, 5, 8, 6, 6, -3, 5, 2]

    fenwick_tree = FenwickTree(a)

    print('Cumulative sum')
    print('get_cumulative_sum(1): %d' % fenwick_tree.get_cumulative_sum(1))
    print('get_cumulative_sum(3): %d' % fenwick_tree.get_cumulative_sum(3))
    print('get_cumulative_sum(5): %d' % fenwick_tree.get_cumulative_sum(5))
    print('get_cumulative_sum(9): %d' % fenwick_tree.get_cumulative_sum(9))
    print('get_cumulative_sum(15): %d' % fenwick_tree.get_cumulative_sum(15))

    print('\n')
    print('Single item')
    print('get(5): %d' % fenwick_tree.get(5))

    print('\n')
    print('Add value')
    print('get(5): %d' % fenwick_tree.get(5))
    fenwick_tree.add_value(5, 4)
    print('add_value(5, 4): %d' % fenwick_tree.get(5))

    print('\n')
    print('Find')
    print('find(10): %d' % fenwick_tree.find(10))

    print('\n')
    print('Scale by 3')
    fenwick_tree.scale(3)
    print('get(5): %f' % fenwick_tree.get(5))

