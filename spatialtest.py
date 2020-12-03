import unittest
import numpy as np

# Imports defined functions
import sys
sys.path.append("../")
from sir.discretemodelspatial import *

class TestDiscreteSpatialMethod(unittest.TestCase):

    def test_change_pos(self):
        """
        Tests the position is within the grid [0,1]x[0,1]
        """
        agent = Agent()
        for i in range(100):
            agent.change_pos()
            self.assertTrue(0 <= agent.pos[0] <= 1)
            self.assertTrue(0 <= agent.pos[1] <= 1)

    def test_susc(self):
        """
        Tests that Agent class returns 'S'
        """
        agent = Agent()
        self.assertEqual(agent.state, 'S')

    def test_inf(self):
        """
        Tests that Agent class returns 'I'
        """
        agent = Agent()
        agent.change_state()
        self.assertEqual(agent.state, 'I')

    def test_rec(self):
        """
        Tests that Agent class returns 'R'
        """
        agent = Agent()
        agent.change_state()
        agent.change_state()
        self.assertEqual(agent.state, 'R')

    def test_sum(self):
        """
        Tests that S+I+R = N
        """
        qs = [0.1, 0.2, 0.3]
        ks = [0.01, 0.02, 0.03]
        ts = [10, 20, 30]
        ns = [10, 20, 30]
        pos = [False, 'middle', 'corner']

        for q in qs:
            for k in ks:
                for t in ts:
                    for n in ns:
                        for p in pos:
                            counts_sus, counts_inf, counts_rec = discrete_spatial_simulation(k, q, t=t, n=n, position=p)
                            for i in range(len(counts_sus)):
                                cts = counts_sus[i] + counts_inf[i] + counts_rec[i]
                                self.assertEqual(cts, n)