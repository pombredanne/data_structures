from random import random
from math import ceil


__author__ = 'Paul Tune'
__date__ = '05 Feb 2016'


class FrugalSketches():
    """
    Implementation of very low memory sketches for estimating quantiles in data streams. These
    algorithms were developed by Qiang et al. [1]. Designation of U determines memory unit usage
    (a memory unit is defined as the maximum word size required to hold the value of the quantile of
    the data stream).

    References:
    1. Q. Ma, S. Muthhukrishnan and M. Sandler, "Frugal Streaming for Estimating Quantiles", Space
       Efficient Data Structures, Streams and Algorithms, Festchrift in Honor of J. Ian Munro,
       Andrej Brodnik, Alejandro Lopez-Ortiz, Venkatesh Raman and Alfredo Viola (Eds.), LNCS 8066,
       Springer, 2013.
    """
    def __init__(self, count=0, h=1, k=2, f=lambda x: x):
        """
        Initialize the sketch. See the class functions for usage examples.

        :param count: initial value of counter to estimate quantile
        :param h: h-th
        :param k: of k-th quantile
        :return: an instance of a sketch
        """
        self.count = count
        self.threshold = float(h)/k
        self.step = 1
        self.sign = 1
        self.f = f

    def frugal1U_median(self, s):
        """
        Estimate median with one unit of memory. Example usage:

        >>test_stream = [3,2,1,4,5]
        >>fgsk = FrugalSketches()
        >>stream_data(test_stream, fgsk.frugal1U_median)
        >>print(fgsk.get_statistic())
        3

        :param s: item in data stream
        """
        if s > self.count:
            self.count += 1
        elif s < self.count:
            self.count -= 1

    def frugal1U(self, s):
        """
        Estimate h-th k-th quantile, defined as the value x such that Pr(X < x) = h/k, where X is a random variable
        in the domain of integers (though non-integers can be used too, by rewriting and converting to integers). Only
        one unit of memory is used.

        Example usage:

        >>test_stream = [3,2,1,4,5]
        >>fgsk = FrugalSketches(h=1, k=4)
        >>stream_data(test_stream, fgsk.frugal1U)
        >>print(fgsk.get_statistic())
        1

        :param s: item in data stream
        """
        r = random()

        if s > self.count and r > 1 - self.threshold:
            self.count += 1
        elif s < self.count and r > self.threshold:
            self.count -= 1

    def frugal2U(self, s):
        """
        Estimate h-th k-th quantile, defined as the value x such that Pr(X < x) = h/k, where X is a random variable
        in the domain of integers (though non-integers can be used too, by rewriting and converting to integers).
        Better estimation than frugal1U, but longer "burn-in" time, i.e., the stream must be long in order for estimates
        to converge.

        Example usage:

        >>test_stream = [3,2,1,4,5]
        >>dbl_update = lambda x: 2*x
        >>fgsk = FrugalSketches(h=1, k=4, f=dbl_update)
        >>stream_data(test_stream, fgsk.frugal2U)
        >>print(fgsk.get_statistic())
        1

        :param s: item in data stream
        :param f: function that determines step size of increments/decrements
        """

        r = random()

        if s > self.count and r > 1 - self.threshold:
            self.step += self.f(self.step) if self.sign > 0 else -self.f(self.step)
            self.count += ceil(self.step) if self.step > 0 else 1
            self.sign = 1

            if self.count > s:
                self.step += s - self.count
                self.count = s
        elif s < self.count and r > self.threshold:
            self.step += self.f(self.step) if self.sign < 0 else -self.f(self.step)
            self.count -= ceil(self.step) if self.step > 0 else 1
            self.sign = -1

            if self.count < s:
                self.step += self.count - s
                self.count = s

        if (self.count - s) < 0 and self.step > 1:
            self.step = 1

    def get_statistic(self):
        """
        Return quantile estimate.

        :return: quantile estimate
        """
        return self.count


def stream_data(stream, sketch):
    """
    Stream the data with chosen sketch.

    :param stream: data stream
    :param sketch: chosen sketch
    """
    for s in stream:
        # update sketch
        sketch(s)

