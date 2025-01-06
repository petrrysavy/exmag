import unittest

import numpy as np
import numpy.testing as npt

from dagsolvers.solve_exmag import *


def normalize_data(X):
    mean = np.mean(X, axis=0)
    std = np.std(X, axis=0)
    X = X - mean
    X = X / std
    return X


class TestRun(unittest.TestCase):

    def test_default(self):
        tabu_edges = [(0, 1)]
        X = np.array([[0.0203909, 0.04775229],
                     [0.25638959, 0.50334587],
                     [0.20186161, 0.40688697],
                     [0.42097784, 0.83867313],
                     [0.56834260, 1.13922780],
                     [0.04024122, 0.09041621],
                     [0.42283032, 0.84356574],
                     [0.67292356, 1.34925317],
                     [0.16439640, 0.30947817],
                     [0.81765796, 1.62457809]])
        X = normalize_data(X)

        # W_est, A_est, _, _, stats = solve(X, cfg, 0, Y=Y, B_ref=None)
        W_est, W_bi, _, _, stats = solve(X, lambda1=1, loss_type='l2', reg_type='l1', w_threshold=0,
                                         tabu_edges=tabu_edges, B_ref=None, mode='all_cycles')

        print(W_est)
        print(W_bi)


if __name__ == '__main__':
    unittest.main()
