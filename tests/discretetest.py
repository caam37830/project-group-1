import unittest
from ../sir/discrete import *

class TestDiscreteMethod(unittest.TestCase):
    def __init__(self):
        self.agent = Agent()

    def test_susc(self):
        """
        Tests that Agent class returns susceptible = True
        """
        self.assertEqual(self.agent.is_susceptible(), True)
        self.assertEqual(self.agent.is_infected(), False)
        self.assertEqual(self.agent.is_recovered(), False)

    def test_inf(self):
        """
        Tests that Agent class returns infected = True
        """
        self.agent.infect()
        self.assertEqual(self.agent.is_susceptible(), False)
        self.assertEqual(self.agent.is_infected(), True)
        self.assertEqual(self.agent.is_recovered(), False)


    def test_rec(self):
        """
        Tests that Agent class returns recovered = True
        """
        self.agent.recover()
        self.assertEqual(self.agent.is_susceptible(), False)
        self.assertEqual(self.agent.is_infected(), True)
        self.assertEqual(self.agent.is_recovered(), False)

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
                        cts = counts_sus + counts_inf + counts_rec
                        self.assertEqual(cts, n)

