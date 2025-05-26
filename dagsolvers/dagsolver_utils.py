import networkx as nx
import numpy as np
from networkx import from_numpy_array, DiGraph

import notears.utils as notears_utils


def apply_threshold(W, w_threshold):
    W_t = np.copy(W)
    W_t[np.abs(W) < w_threshold] = 0
    return W_t


def find_minimal_dag_threshold(W):
    if notears_utils.is_dag(W):
        return 0, W
    possible_thresholds = sorted((abs(t) for t in W.flatten() if abs(t) > 0))
    for t_candidate in possible_thresholds:
        W[np.abs(W) < t_candidate] = 0
        if notears_utils.is_dag(W):
            return t_candidate, W
    assert False  # Should always find a dag


def find_optimal_threshold_for_shd(B_true, W_est, A_true, A_est, W_bi_true, W_bi_est):
    values = set((abs(t) for t in W_est.flatten() if abs(t) > 0))
    for A_i_est in A_est:
        values.update((abs(t) for t in A_i_est.flatten() if abs(t) > 0))

    possible_thresholds = values #sorted((abs(t) for t in W_est.flatten() if abs(t) > 0))
    if not possible_thresholds:
        possible_thresholds = [0]

    best_t = max(possible_thresholds) if possible_thresholds else 0
    best_shd = B_true.shape[0] ** 2 # calculate_shd(W_true, W_est != 0, A_true, A_est) # W_true.shape[0]**2
    B_bi_true = W_bi_true != 0
    B_all_true = B_true - B_bi_true
    for t_candidate in possible_thresholds:
        W_est_t = apply_threshold(W_est, t_candidate)
        A_est_t = [apply_threshold(A_i_est, t_candidate) for A_i_est in A_est]
        W_bi_est_t = apply_threshold(W_bi_est, t_candidate)
        B_bi_est_t = (W_bi_est_t != 0)
        B_est_t = W_est_t != 0
        B_all_est_t = B_est_t + (-1 * B_bi_est_t) # CPDAG - undirected edges have -1
        shd, _, _ = calculate_shd(B_all_true, B_all_est_t, A_true, A_est_t)

        if shd < best_shd:
            best_t = t_candidate
            best_shd = shd
    return best_t, best_shd


def calculate_dag_shd(B_true, B_est, test_dag=True):
    assert B_true.shape == B_est.shape
    if (B_est == -1).any():  # cpdag
        if not ((B_est == 0) | (B_est == 1) | (B_est == -1)).all():
            raise ValueError('B_est should take value in {0,1,-1}')
        if ((B_est == -1) & (B_est.T == -1)).any():
            raise ValueError('undirected edge should only appear once')
    else:  # dag
        if not ((B_est == 0) | (B_est == 1)).all():
            raise ValueError('B_est should take value in {0,1}')
        if test_dag and not notears_utils.is_dag(B_est):
            raise ValueError('B_est should be a DAG')

    shd = 0
    for i in range(B_true.shape[0]):
        for j in range(i):
            e_ij = (B_est[i,j], B_est[j,i])
            if min(e_ij) == -1:
                e_ij = (-1,-1)
            t_ij = (B_true[i,j], B_true[j,i])
            if min(t_ij) == -1:
                t_ij = (-1,-1)

            if e_ij != t_ij:
                if e_ij == t_ij[::-1]:
                    shd += 0.5
                elif (e_ij == (-1,-1) and t_ij == (0,0)) or (e_ij == (0,0) and t_ij == (-1,-1)):
                    shd += 1
                elif e_ij == (-1, -1) or t_ij == (-1, -1):
                    shd += 0.5
                else:
                    shd += 1

    return shd


def calculate_shd(B_true, B_est, A_true, A_est, test_dag=True):
    shd = calculate_dag_shd(B_true, B_est, test_dag=test_dag)
    a_shd = 0
    for i in range(len(A_true)):
        a_i_shd = calculate_dag_shd(A_true[i] != 0, A_est[i] != 0, test_dag=False)
        a_shd += a_i_shd
    return shd + a_shd, shd, a_shd


def least_square_cost(X, W):
    n, d = X.shape
    val = sum((X[i,j] - sum(X[i, k] * W[k, j] for k in range(d) if k != j))**2 for i in range(n) for j in range(d))
    return val


def plot(W, filename=None):
    import matplotlib.pyplot as plt
    # if abbrev:
    #     ls = dict((x,x[:3]) for x in self.nodes)
    # else:
    #     ls = None
    # try:
    #     edge_colors = [self._edge_colour[compelled] for (u,v,compelled) in self.edges.data('compelled')]
    # except KeyError:
    #     edge_colors = 'k'
    graph = from_numpy_array(W, create_using=DiGraph)
    fig, ax = plt.subplots()
    nx.draw_networkx(graph, ax=ax, pos=nx.drawing.nx_agraph.graphviz_layout(graph,prog='dot'),
                     node_color="white",arrowsize=15)
    if filename is not None:
        fig.savefig(filename,format='png', bbox_inches='tight')
    else:
        plt.show()


def tupledict_to_np_matrix(tuple_dict, d):
    matrix = np.zeros((d, d))
    for (i, j), value in tuple_dict.items():
        matrix[i, j] = value
    return matrix
