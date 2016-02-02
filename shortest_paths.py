import numpy as np
import sys
from heapq import heappop, heappush

__author__ = 'Paul Tune'
__date__ = '19 Jan 2016'

# TODO: negative cycle detection?
def floyd(n, weight_mtx):
    """
    Classic Floyd-Warshall all shortest paths algorithm. Also returns the predecessor matrix.

    :param weight_mtx: matrix of link weights
    :return: distance matrix and predecessor matrix
    """
    # initialize
    dist_mtx = sys.maxsize*np.ones((n, n)) # set to MAXSIZE
    pred_mtx = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if weight_mtx[i][j] != sys.maxsize:
                dist_mtx[i][j] = weight_mtx[i][j]
                pred_mtx[i][j] = i
        # ensure consistency
        dist_mtx[i][i] = 0
        pred_mtx[i][i] = -1

    # classic Floyd-Warshall algorithm
    for k in range(n):
        for j in range(n):
            for i in range(n):
                test_dist = dist_mtx[i][k] + dist_mtx[k][j]
                if test_dist < dist_mtx[i][j]:
                    # update distance matrix
                    dist_mtx[i][j] = test_dist
                    # update predecessor matrix
                    pred_mtx[i][j] = pred_mtx[k][j]

    return dist_mtx, pred_mtx


# TODO: implement Bellman-Ford
def dijkstra(n, weight_mtx):
    """
    Classic Dijkstra all shortest paths algorithm. Heap-based implementation.

    :param weight_mtx: matrix of link weights (must be non-negative)
    :return: distance matrix and predecessor matrix
    """
    # initialize
    dist_mtx = sys.maxsize*np.ones((n, n)) # set to MAXSIZE
    pred_mtx = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            pred_mtx[i][j] = i
        # ensure consistency
        dist_mtx[i][i] = 0
        pred_mtx[i][i] = -1

    # compute for each source to get all shortest paths
    for source in range(n):
        # reset
        marked = {source: True}
        final_dist = {}  # to check if there are potentially negative weights
        heap = []

        # Dijkstra's algorithm starts here
        # initializing heap/priority queue with source, we know distance must be 0
        heappush(heap, (0, source))

        # while heap is not empty
        while heap:
            dist, k = heappop(heap)
            # this is one way without having to decrease priority
            if k in final_dist: continue

            dist_mtx[source][k] = dist
            final_dist[k] = dist  # keeps the list of optimal distances
            marked[k] = True

            # check all neighbors of k
            for j in range(n):
                # check if they are connected and not equal to itself
                if j != k and j not in marked:
                    alt_path_dist = dist_mtx[source][k] + weight_mtx[k][j]

                    # for all neighbors of k
                    if j in final_dist:
                          if alt_path_dist < final_dist[j]:
                            raise ValueError("Potential negative weights in links")
                    # must have not seen this and it's distance may be shorter
                    elif alt_path_dist < dist_mtx[source][j]:
                            heappush(heap, (alt_path_dist, j))
                            pred_mtx[source][j] = k

    return dist_mtx, pred_mtx
