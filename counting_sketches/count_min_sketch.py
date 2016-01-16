try:
    import xxhash
except:
    raise ImportError('count_min_sketch requires xxhash >= 0.4.3')

from array import array
# math functions used to compute the size based on error and error
# probability
from math import log, ceil, exp


__date__ = '16 Jan 2015'
__author__ = 'Paul Tune'


class CountMinSketch:
    """
    A sketch to return the count of a unique item, developed by Cormode and Muthukrishnan
    for the cash register model. All item counts must be non-negative. Essentially a
    two-dimensional hash table. Allows point query of unique items stored in the sketch.

    There are two ways to  construct CountMinSketch:

        1. set row_col=True: param1 and param2 are the number of rows and columns respectively,
        2. set row_col=False: param1 and param2 are the error margin and error probability
        respectively. The rows and columns are computed based on bounds in Cormode and
        Muthukrishnan's paper.

    Initialization examples:

        from count_min_sketch import CountMinSketch
        sketch = CountMinSketch(1000, 10)  # 1000 rows, 10 columns
        sketch2 = CountMinSketch(0.1, 0.01, row_col=False) # 0.1 error, 0.01 error probability

    Usage examples:

        sketch.update("Hillary")           # adds item "Hillary" with count 1 (default)
        sketch.update("Hillary", value=5)  # adds 5 counts to item "Hillary"
        sketch.update(tuple())             # adds a tuple() object with count 1


        # conservative update, like update() but maintains more accurate counts
        # with slightly extra overhead
        sketch.csv_update("John")

        print(sketch.query("John"))         # prints 1
        print(sketch["Hillary"])            # prints 6
        print(sketch[tuple()])              # prints 1

    This implementation uses xxhash for the purpose of speed, as a non-cryptographic hash
    function has a higher processing rate. xxhash has been demonstrated to have high
    performance. This implementation borrows some ideas from Rafa Carrascosa,
    https://github.com/rafacarrascosa/countminsketch
    """
    def __init__(self, param1, param2, row_col=True):
        """
        Initializes the Count Min sketch. There are two ways to  construct
        CountMinSketch:

        1. set row_col=True: param1 and param2 are the number of rows and
           columns respectively,
        2. set row_col=False: param1 and param2 are the error margin and
           error probability respectively.

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

    def _hash(self, item):
        # get Python hash ID of object
        # technique used by Rafa Carrascosa
        # https://github.com/rafacarrascosa/countminsketch
        h = xxhash.xxh32(str(hash(item)))
        for i in range(self.num_rows):
            h.update(str(i))
            yield h.intdigest() % self.num_columns

    def update(self, item, count=1):
        """
        Inserts items into the sketch. Item must have a unique ID and a non-negative count.

        :param id: unique ID of item
        :param count: count of the item (default is 1)
        """
        if count < 0:
            raise ValueError('Item has non-negative count')

        if count == 0:
            return

        self.num_items += 1
        for counter, i in zip(self.counters, self._hash(item)):
            counter[i] += count

    def csv_update(self, item, count=1):
        """
        Conservative update is a heuristic which has been proven to improve the
        update procedure, at the cost of slightly more computation. Inserts items
        into the sketch.

        :param id: unique ID of item
        :param count: count of the item (default is 1)
        """
        if count < 0:
            raise ValueError('Item has non-negative count')

        if count == 0:
            return

        self.num_items += 1
        for counter, i in zip(self.counters, self._hash(item)):
            # query the item
            min_val = self.query(id)
            counter[i] = max(counter[i], min_val + count)

    def query(self, item):
        """
        Returns count of queried item.

        :param id: unique ID of item
        :return: count of the item
        """

        return min(counter[i] for counter, i in zip(self.counters, self._hash(item)))

    def __getitem__(self, item):
        """
        Convenience method to return count of queried item.

        :param id: unique ID of item
        :return: count of the item
        """

        return self.query(item)

    def __len__(self):
        """
        Returns number of items stored in sketch.

        :return: number of items
        """
        return self.num_items


class GeneralCountMinSketch:
    """
    The CountMinSketch only works for items with a non-negative count. GeneralCountMinSketch
    circumvents this limitation by composing two CountMinSketches: one to store non-negative
    counts and the other for negative counts.
    """

    def __init__(self, param1, param2, row_col=True):
        self.sketch_positive = CountMinSketch(param1, param2, row_col)
        self.sketch_negative = CountMinSketch(param1, param2, row_col)

    def update(self, item, count=1):
        if count < 0:
            self.sketch_negative.update(item, count)
        else:
            self.sketch_positive.update(item, count)

    def query(self, item):
        return self.sketch_positive.query(item) - self.sketch_negative.query(item)

    def __getitem__(self, item):
        return self.query(item)

    def __len__(self):
        return self.sketch_positive.num_items

def main():
    # data_stream = [(1,2), (4,1)]
    # cms = CountMinSketch(0.1,0.1,row_col=False)
    cms = CountMinSketch(1000, 10)
    cms.csv_update(4, 2)
    cms.csv_update('Hillary', 7)
    print(cms.query(4))
    print(cms.query('Hillary'))

if __name__ == '__main__':
    main()