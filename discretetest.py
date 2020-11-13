import unittest

import numpy as np 
from numpy.random import randint, rand
import matplotlib.pyplot as plt

import sys
sys.path.append("../")
from sir.discretemodel import *

class TestDiscreteMethod(unittest.TestCase):

    def test_susc(self):
        """
        Tests that Agent class returns susceptible = True
        """
        agent = Agent()
        self.assertEqual(agent.is_susceptible(), True)
        self.assertEqual(agent.is_infected(), False)
        self.assertEqual(agent.is_recovered(), False)

    def test_inf(self):
        """
        Tests that Agent class returns infected = True
        """
        agent = Agent()
        agent.infect()
        self.assertEqual(agent.is_susceptible(), False)
        self.assertEqual(agent.is_infected(), True)
        self.assertEqual(agent.is_recovered(), False)


    def test_rec(self):
        """
        Tests that Agent class returns recovered = True
        """
        agent = Agent()
        agent.recover()
        self.assertEqual(agent.is_susceptible(), False)
        self.assertEqual(agent.is_infected(), False)
        self.assertEqual(agent.is_recovered(), True)

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
