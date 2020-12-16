import unittest
import sys
sys.path.append("../")
from sir.discretemodel import *

class TestDiscreteMethod(unittest.TestCase):

    def test_susc(self):
        """
        Tests that Agent class returns susceptible = True
        """
        agent = Agent()
        self.assertEqual(agent.state, 'S')


    def test_inf(self):
        """
        Tests that Agent class returns infected = True
        """
        agent = Agent()
        agent.change_state()
        self.assertEqual(agent.state, 'I')


    def test_rec(self):
        """
        Tests that Agent class returns recovered = True
        """
        agent = Agent()
        agent.change_state()
        agent.change_state()
        self.assertEqual(agent.state, 'R')

    def test_sum(self):
        """
        Tests that S+I+R = N
        """
        bs = [0.1, 0.2, 0.3]
        ks = [0.01, 0.02, 0.03]
        ts = [10, 20, 30]
        ns = [10, 20, 30]

        for b in bs:
            for k in ks:
                for t in ts:
                    for n in ns:
                        counts_sus, counts_inf, counts_rec = run_simulation(b, k, N=n, T=t)
                        for i in range(len(counts_sus)):
                            cts = counts_sus[i] + counts_inf[i] + counts_rec[i]
                            self.assertEqual(cts, n)