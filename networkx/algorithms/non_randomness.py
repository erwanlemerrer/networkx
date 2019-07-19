# -*- coding: utf-8 -*-
#    Copyright (C) 2004-2019 by
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Pieter Swart <swart@lanl.gov>
#    All rights reserved.
#    BSD license.
#
# Authors: Erwan  Le Merrer (erwan.le-merrer@inria.fr)

r""" Computation of graph non-randomness
"""

import math
import networkx as nx

__all__ = ['non_randomness']


def non_randomness(G, k=None):
    """Compute the non-randomness of graph G.

    The first returned value nr is the sum of non-randomness values of all
    edges within the graph (where the non-randomness of an edge tends to be
    small when the two nodes linked by that edge are from two different
    communities).

    The second computed value nr_rd is a relative measure that indicates
    to what extent graph G is different from random graphs in terms
    of probability. When it is close to 0, the graph tends to be more
    likely generated by an Erdos Renyi model.

    Parameters
    ----------
    G : NetworkX graph

    k : int
        The number of communities in G.
        If k is not set, the function will use a default community
        detection algorithm to set it.

    Returns
    -------
    non-randomness : (float, float) tuple
        Non-randomness, Relative non-randomness w.r.t.
        Erdos Renyi random graphs.

    Examples
    --------
    >>> G = nx.karate_club_graph()
    >>> nr, nr_rd = nx.non_randomness(G, 2)

    Notes
    -----
    This computes Eq. (4.4) and (4.5) in Ref. [1]_.

    References
    ----------
     .. [1] Xiaowei Ying and Xintao Wu,
            On Randomness Measures for Social Networks,
            SIAM International Conference on Data Mining. 2009
    """

    if k is None:
        k = len(tuple(nx.community.label_propagation_communities(G)))

    try:
        import numpy as np
    except ImportError:
        msg = "non_randomness requires NumPy: http://scipy.org/"
        raise ImportError(msg)

    # eq. 4.4
    nr = np.real(np.sum(np.linalg.eigvals(nx.to_numpy_matrix(G))[:k]))

    n = G.number_of_nodes()
    m = G.number_of_edges()
    p = (2 * k * m) / (n * (n - k))

    # eq. 4.5
    nr_rd = (nr - ((n - 2 * k) * p + k)) / math.sqrt(2 * k * p * (1 - p))

    return nr, nr_rd


# fixture for nose tests
def setup_module(module):
    from nose import SkipTest
    try:
        import numpy
    except:
        raise SkipTest("NumPy not available")
