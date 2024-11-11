import unittest

from parameterized import parameterized
import numpy as np
import numpy.testing as npt

from dagsolvers.magseparation import *


# an example build on https://proceedings.mlr.press/v161/rantanen21a/rantanen21a.pdf, figure 1, a + b
# vertices are in order q, x, y, w
Q = 0
X = 1
Y = 2
W = 3
D = 4


def matrix_from_edges(edges, d, bidirect=False):
    adj_matrix = np.zeros((d, d), dtype=int)
    for i, j in edges:
        adj_matrix[i, j] = 1
        if(bidirect):
            adj_matrix[j, i] = 1
    return adj_matrix


GRAPH_1_EDG = matrix_from_edges([(W, X), (Q, Y)], D)
GRAPH_1_BIEDG = matrix_from_edges([(X, Q), (Y, W)], D, bidirect=True)
GRAPH_1_FW = GRAPH_1_EDG.astype(float)
GRAPH_1_FW[GRAPH_1_FW == 0] = np.inf

GRAPH_2_EDG = matrix_from_edges([(Y, X), (W, Q)], D)
GRAPH_2_BIEDG = matrix_from_edges([(X, W), (Y, W), (W, Q)], D, bidirect=True)
GRAPH_2_FW = GRAPH_2_EDG.astype(float)
GRAPH_2_FW[GRAPH_2_FW == 0] = np.inf


class TestMAGSeaparator(unittest.TestCase):

    @parameterized.expand([
        (GRAPH_1_EDG, GRAPH_1_FW),
        (GRAPH_2_EDG, GRAPH_2_FW)
    ])
    def test_floyd_warshall(self, adj, fwdist):
        npt.assert_array_equal(floyd_warshall(adj), fwdist)


if __name__ == '__main__':
    unittest.main()
