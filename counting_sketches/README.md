# Counting Sketches
A collection of useful data streaming sketches for counting items in a data
stream.

**CountMinSketch**

A sketch to return the count of a unique item, developed by Cormode and Muthukrishnan
for the cash register model. All item counts must be non-negative. Essentially a
two-dimensional hash table. Allows point query of unique items stored in the sketch.

Depends on [xxhash](https://pypi.python.org/pypi/xxhash/) version 0.4.3 and above. xxhash was chosen for its fast
performance as it is a non-cryptographic hash function. 

1. Cormode, G., Muthukrishnan, S. An Improved Data Stream Summary: The Count-Min Sketch and its Applications. J. Algorithms 55,
(2005), 29–38.

**TugOfWarSketch**

The Tug-of-War Sketch estimates the second moment of a data stream in logarithmic space. This 
is a minimalistic implementation which has no dependencies because it uses the MD5 hash 
(which admittedly is slow). Modification to using the Murmur hash or xxhash can be done easily.

1. Alon N., Matias Y., Szegedy M. The space complexity of approximating the frequency moments. J. Comput. System Sci. (1996) pp. 20-29.
2. Chakrabarti A. CS49: Data Stream Algorithms, Lecture Notes, Fall 2011. Chapter 6.

**ApproximateCounting**

Classic Morris counter sketch that was analyzed in detail by Phillipe Flajolet. Used to count large frequencies of items in small 
registers. Precursor to modern sketches.

1. Morris, R. Counting large numbers of events in small registers. Communications of the ACM 21, 10 (1977), 840–842.
2. Flajolet, P. Approximate Counting: A Detailed Analysis. BIT 25, (1985), 113-134.

**FrugalSketches**

Low memory sketches to estimate quantiles in a datastream, specifically, the median and the h-th k-th quantile, which is
defined as the x such that Pr(X < x) = h/k. Requires only a single or two memory units, where a memory unit is defined as a sufficient
bits to store the input stream's domain. Works on set of integers distributed over {1,2,...,N} (rescaling is required for a data
stream of floating point numbers).

1. Ma Q., Muthhukrishnan S., Sandler M. Frugal Streaming for Estimating Quantiles. Space Efficient Data Structures, Streams and 
Algorithms, Festchrift in Honor of J. Ian Munro, Andrej Brodnik, Alejandro Lopez-Ortiz, Venkatesh Raman and Alfredo Viola (Eds.), LNCS
8066, Springer, 2013.
