import unittest
import sys
sys.path.append("../")
from sir.stochasticsir import *

class TestStochasticMethod(unittest.TestCase):

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
        ps = [0.1, 0.01, 0.5]
        Rs = [3, 10, 1]
        ns = [10, 20, 30]

        for p in ps:
            for R in Rs:
                for n in ns:
                    counts_sus1, counts_inf1, counts_rec1, t1 = stochastic_constant_contacts(p, R, N=n)
                    counts_sus2, counts_inf2, counts_rec2, t2 = stochastic_fixed_contacts(p, R, N=n)
                    counts_sus3, counts_inf3, counts_rec3, t3 = stochastic_random_contacts(p, R, N=n)
                    for i in range(len(counts_sus1)):
                        cts = counts_sus1[i] + counts_inf1[i] + counts_rec1[i]
                        self.assertEqual(cts, n)
                    for j in range(len(counts_sus2)):
                        cts2 = counts_sus2[j] + counts_inf2[j] + counts_rec2[j]
                        self.assertEqual(cts2, n)
                    for k in range(len(counts_sus3)):
                        cts3 = counts_sus3[k] + counts_inf3[k] + counts_rec3[k]
                        self.assertEqual(cts3, n)
        
    def stop_simulation(self):
        """
        tests that the simulation functions stop immediately after epidemic ends
        """
        ps = [0.1, 0.01, 0.5]
        Rs = [3, 10, 1]
        ns = [10, 20, 30]

        for p in ps:
            for R in Rs:
                for n in ns:
                    counts_sus, counts_inf, counts_rec, t = stochastic_constant_contacts(p, R, N=n)
                    self.assertEqual(counts_inf[-1], 0)
                    self.assertTrue(counts_inf[-2]>0)
    
    def duration(self):
        """
        tests that the function returns the right duration
        """
        ps = [0.1, 0.01, 0.5]
        Rs = [3, 10, 1]
        ns = [10, 20, 30]

        for p in ps:
            for R in Rs:
                for n in ns:
                    counts_sus, counts_inf, counts_rec, t = stochastic_constant_contacts(p, R, N=n)
                    self.assertEqual(len(counts_inf), t)
                    self.assertEqual(len(counts_sus), t)
                    self.assertEqual(len(counts_rec), t)

