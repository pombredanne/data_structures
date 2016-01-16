try:
    import xxhash
except:
    raise ImportError('count_min_sketch requires xxhash >= 0.4.3')

from array import array
from math import log, ceil, exp


__date__ = '16 Jan 2015'
__author__ = 'Paul Tune'


class CountMinSketch:
    """
    A sketch to return the count of a unique item.

    The sketch was implemented using xxhash for the purpose of speed, as a non-cryptographic hash
    function has a higher processing rate.

    """
    def __init__(self, param1, param2, row_col=True):
        """
        Initializes the Count Min sketch.

        :param param1: number of rows or error margin parameter
        :param param2: number of columns or error probability parameter
        :param row_col: set to True to specify rows/columns, False for
            error margin/error probability. Default is True
        """
        if row_col:
            if param1 < 2 or param2 < 2:
                raise ValueError('Rows and/or columns must be greater than 2')

            self._row_col_construction(param1, param2)
        else:
            if not 0 < param1 < 1:
                raise ValueError('Error must be between 0 and 1')
            if not 0 < param2 < 1:
                raise ValueError('Error probability must be between 0 and 1')

            self._error_bound_construction(param1, param2)


    @classmethod
    def _error_bound_construction(cls, error, error_prob):
        cls.num_rows = int(ceil(-log(error_prob)))
        cls.num_columns = int(ceil(exp(1)/error))
        cls.num_items = 0
        cls.counters = []

        # build the table of counters
        for _ in range(cls.num_rows):
            counter = array("l", (0 for _ in range(cls.num_columns)))
            cls.counters.append(counter)

        return cls

    @classmethod
    def _row_col_construction(cls, rows, cols):
        cls.num_rows = rows
        cls.num_columns = cols
        cls.num_items = 0
        cls.counters = []

        # build the table of counters
        for _ in range(cls.num_rows):
            counter = array("l", (0 for _ in range(cls.num_columns)))
            cls.counters.append(counter)

        return cls

    def _hash(self, id):
        # get Python hash ID of object
        # technique used by Rafa Carrascosa
        # https://github.com/rafacarrascosa/countminsketch
        h = xxhash.xxh32(str(hash(id)))
        for i in range(self.num_rows):
            h.update(str(i))
            yield h.intdigest() % self.num_columns

    def update(self, id, count=1):
        """
        Inserts items into the sketch. Item must have a unique ID and a non-negative count.

        :param id: unique ID of item
        :param count: count of the item (default is 1)
        """
        if count < 0:
            raise ValueError('Item has non-negative count')

        self.num_items += 1
        for counter, i in zip(self.counters, self._hash(id)):
            counter[i] += count

    def conservative_update(self, id, count=1):
        """
        Conservative update is a heuristic which has been proven to improve the
        update procedure, at the cost of slightly more computation. Inserts items
        into the sketch.

        :param id: unique ID of item
        :param count: count of the item (default is 1)
        """
        if count < 0:
            raise ValueError('Item has non-negative count')

        self.num_items += 1
        for counter, i in zip(self.counters, self._hash(id)):
            # query the item
            min_val = self.query(id)
            counter[i] = max(counter[i], min_val + count)

    def query(self, id):
        return min(counter[i] for counter, i in zip(self.counters, self._hash(id)))

    def __len__(self):
        return self.num_items

def main():
    # data_stream = [(1,2), (4,1)]
    # cms = CountMinSketch(0.1,0.1,row_col=False)
    cms = CountMinSketch(1000,10)
    cms.conservative_update(4,2)
    cms.conservative_update('Hillary', 7)
    print(cms.query(4))
    print(cms.query('Hillary'))

if __name__ == '__main__':
    main()