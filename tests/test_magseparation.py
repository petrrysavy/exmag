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
        if bidirect:
            adj_matrix[j, i] = 1
    return adj_matrix


GRAPH_1_EDG = matrix_from_edges([(W, X), (Q, Y)], D)
GRAPH_1_BIEDG = matrix_from_edges([(X, Q), (Y, W)], D, bidirect=True)
GRAPH_1_FW = GRAPH_1_EDG.astype(float)
GRAPH_1_FW[GRAPH_1_FW == 0] = np.inf
np.fill_diagonal(GRAPH_1_FW, 0)

GRAPH_2_EDG = matrix_from_edges([(Y, X), (W, Q)], D)
GRAPH_2_BIEDG = matrix_from_edges([(X, W), (Y, W), (W, Q)], D, bidirect=True)
GRAPH_2_FW = GRAPH_2_EDG.astype(float)
GRAPH_2_FW[GRAPH_2_FW == 0] = np.inf
np.fill_diagonal(GRAPH_2_FW, 0)

GRAPH_3_EDG = matrix_from_edges([(X, Y), (Y, Q), (Q, W), (Y, W)], D)
GRAPH_3_FW = [
    [0, np.inf, np.inf, 1],  # Q
    [2, 0, 1, 2],  # X
    [1, np.inf, 0, 1],  # Y
    [np.inf, np.inf, np.inf, 0]  # W
]


class TestMAGSeaparator(unittest.TestCase):

    @parameterized.expand([
        (GRAPH_1_EDG, GRAPH_1_FW),
        (GRAPH_2_EDG, GRAPH_2_FW),
        (GRAPH_3_EDG, GRAPH_3_FW)
    ])
    def test_floyd_warshall(self, adj, fwdist):
        npt.assert_array_equal(floyd_warshall(adj), fwdist)

    @parameterized.expand([
            (GRAPH_1_FW, W, X, [(W, X)]),
            (GRAPH_1_FW, X, W, []),
            (GRAPH_1_FW, Q, W, []),
            (GRAPH_2_FW, Y, X, [(Y, X)]),
            (GRAPH_2_FW, X, Y, []),
            (GRAPH_2_FW, Q, W, []),
            (GRAPH_3_FW, X, Q, [(Y, Q), (X, Y)]),
            (GRAPH_3_FW, X, W, [(X, Y), (Y, Q), (Q, W), (Y, W)]),
            (GRAPH_3_FW, Y, Q, [(Y, Q)]),
            (GRAPH_3_FW, Y, X, [])
    ])
    def test_trace_fw_dist(self, fwdist, u, v, edges):
        self.assertEqual(set(trace_f_w(fwdist, u, v)), set(edges))

    @parameterized.expand([
        (GRAPH_1_EDG, GRAPH_1_BIEDG, GRAPH_1_FW, []),
        (GRAPH_2_EDG, GRAPH_2_BIEDG, GRAPH_2_FW, [([(Y, X), (W, Q)], [(X, W), (Y, W), (W, Q)])])
    ])
    def test_check_for_inducing_path(self, adj, adjbi, fwdist, paths):
        result = check_for_inducing_path(adj, adjbi, fwdist)
        result = set((frozenset(edges), frozenset(frozenset({u, v}) for u, v in biedges)) for edges, biedges in result)
        paths = set((frozenset(edges), frozenset(frozenset({u, v}) for u, v in biedges)) for edges, biedges in paths)
        self.assertEqual(result, paths)


if __name__ == '__main__':
    unittest.main()
