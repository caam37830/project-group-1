import unittest
import numpy as np
# Imports defined functions
import sys
sys.path.append("../")
from sir.spatialextension import *

class TestSpatialExtension(unittest.TestCase):

    def test_sums(self):
        """
        Does three tests that the population always sums to 1 for  the population output, S, I and R and clusterize
        We expect perturbation of data as ks get larger, so tolerances would need to be adjusted
        """
        ks = [10, 10]
        ps = [[1, 0.5], [0.5, 1]]
        S, I, R, S_agg, I_agg, R_agg, pop = simulation(ks,
                                                       ps,
                                                       0.75,
                                                       0.05,
                                                       1000,
                                                       pop_dist=None,
                                                       inf_dist=None,
                                                       inf_rate=0.02)
        # Test 1: Sum SIR
        for i in range(len(S_agg)):
            self.assertTrue(abs(S_agg[i] + I_agg[i] + R_agg[i] - 1) < 0.01) # test S+I+R always sums to 1

        # Test 2: Sum pop
        self.assertTrue(abs(1 - sum(pop)) < 0.01)

        # Test 3: Sum clusters
        S_c, I_c, R_c = clusterize(ks, S, I, R, pop)
        for i in range(len(S_c)):
            for j in range(len(ks)):
                self.assertTrue(abs(S_c[i][j] + I_c[i][j] + R_c[i][j] - 1) < 0.01)

    def test_graph(self):
        """
        Tests that measure adj_matrix is symmetric
        That length of matrix is equal to sum of k
        No entries of M are greater than 1
        """
        # Test 1: Adjacency matrix is symmetric
        ks = [5, 5]
        ps = [[1, 0.5], [0.5, 1]]
        model = SpatialSparse()
        model.gen_graph(ks, ps)
        adj = nx.linalg.adj_matrix(model.G).todense()
        for i in range(model.n):
            for j in range(model.n):
                self.assertEqual(adj[i, j], adj[j, i])

        # Test 2: Sum of ks = len(G)
        self.assertEqual(sum(ks), len(model.G))

        # Test 3: No entries of M are greater than 1
        for i in model.M:
            for j in i:
                self.assertTrue(j < 1)