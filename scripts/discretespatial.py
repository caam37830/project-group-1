"""
This document contains the code for the Discrete Spatial SIR Model
"""

import sys
sys.path.append("../")
from sir.discretemodel import *
import numpy as np 
from numpy.random import randint, rand
import matplotlib.pyplot as plt
from sir.discretemodelspatial import *

# We choose k and b based on the phase diagram from our midterm checkpoint
k = 0.1
b = 0.075
q = np.sqrt(1/(np.pi*100)*b)
p = [0.01, 0.02, 0.03, 0.04, 0.05]
for i in p:
    counts_sus, counts_inf, counts_rec = discrete_spatial_simulation(k, q, p=i, t=100, n=1000, num_agents=10)
    plt.plot(counts_inf, label='p={}'.format(i))
plt.xlabel('t')
plt.ylabel('infected pop')
plt.title('SIR Discrete Spatial w/ different step sizes, p')
plt.legend()
plt.show()
# So we choose p=0.03

k = 0.1
b = 0.075
q = np.sqrt(1/(np.pi*100)*b)
# Random
counts_sus, counts_inf, counts_rec = discrete_spatial_simulation(k, q, p=0.03, t=100, n=1000, num_agents=10)
plt.plot(counts_inf, label='Random')
# Middle
counts_sus, counts_inf, counts_rec = discrete_spatial_simulation(k, q, p=0.03, t=100, n=1000, position='middle', num_agents=10)
plt.plot(counts_inf, label='Middle')
# Corner
counts_sus, counts_inf, counts_rec = discrete_spatial_simulation(k, q, p=0.03, t=100, n=1000, position='corner', num_agents=10)
plt.plot(counts_inf, label='Corner')
plt.xlabel('t')
plt.ylabel('infected pop')
plt.title('SIR random, middle and corner epicenters')
plt.legend()
plt.show()

