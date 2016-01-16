# Counting Sketches
A collection of useful data streaming sketches for counting items in a data
stream.

# CountMinSketch
Depends on xxhash version 0.4.3 and above. xxhash was chosen for its fast
performance as it is a non-cryptographic hash function. 

# ApproximateCounting
Classic Morris counter sketch that was analyzed in detail by Phillipe 
Flajolet. Used to count large frequencies of items in small registers. 
Precursor to modern sketches.

[1] Morris, R. Counting large numbers of events in small registers. Communications of the ACM 21, 10 (1977), 840–842
[2] Flajolet, P. Approximate Counting: A Detailed Analysis. BIT 25, (1985), 113-134 [1]
