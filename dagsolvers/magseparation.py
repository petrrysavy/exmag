import numpy as np


def floydWarshall(adj):
    n = len(adj)
    dist = np.full((n, n), np.inf)

    # initialize the edges from the adj. matrix - inf where adj is zero, 1 otherwise
    dist[adj > 0.5] = 1

    for k in range(n): # k is the midpoint of SP
        for i in range(n):
            for j in range(n):
                len = dist[i][k] + dist[k][j]
                if dist[i][j] > len:
                    dist[i][j] = len

    return dist


def traceFW(dist, u, v):
    if dist[u][v] == np.inf:
        return []

    n = len(dist)
    marked = np.full((n, n), False)
    edges = []
    stack = []
    marked[u,v] = True
    stack.append((u,v))

    while stack:
        i, j = stack.pop()
        for k in range(n):
            if dist[i][k] + dist[k][j] == dist[i][j]: # an SP goes through k
                for s, t in [(i, k), (k, j)]:
                    if not marked[s][t]: # make sure not to include duplicates
                        marked[s][t] = True
                        if dist[s][t] == 1: # direct edge, add it to the list
                            edges.add((s,t))
                        else: # a path, recurse
                            stack.append((s, t))
    return edges

def inducing_path_dfs(dist, adj, s, u, possible_endpoints, path, only_one_dir = True):
    # dist = FW distances, adj = bidirect adjacency, u curr point, s where we started, path = current path
    if len(possible_endpoints) == 0:  # no possible enpoint, how can an inducing path exist?
        return []

    paths = []
    # we need to test for endpoint of the inducing path
    if len(path) > 1:
        if u in possible_endpoints:
            if u < s or not only_one_dir:  # optimization - report only one direction
                paths.append(path)

    # nest further
    n = len(dist)
    for v in range(n):
        if adj[u][v] > 0.5:  # iterate neighbors
            v_endpoints = possible_endpoints if dist[s][v] != np.inf \
                    else possible_endpoints & set(np.where(dist[:][v] > 0.5)[0])  # exists a path to v?
            paths_after_v = inducing_path_dfs(dist, adj, s, v, v_endpoints, path + [v])
            paths.extend(paths_after_v)

    return paths


def inducing_paths(dist, adjbi):
    paths = []
    n = len(dist)
    for v in range(n):
        paths.extend(inducing_path_dfs(dist, adjbi, v, v, set(range(n)), [v]))
    return paths


def check_for_inducing_path(adj, adjbi):
    n = len(adj)
    fwdist = floydWarshall(adj)
    paths = inducing_paths(fwdist, adjbi)
    retval = []  # list of tuples of lists (directed, bidirected)
    for path in paths:
        s = path[0]
        t = path[-1]
        biedges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        diredges = []
        for v in path[1:-1]:
            diredges.extend(traceFW(fwdist, s, v))
            diredges.extend(traceFW(fwdist, t, v))
        retval.append((diredges, biedges))
    return retval
    # todo implmement lazy constraints


