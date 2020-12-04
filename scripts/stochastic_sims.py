"""
This script contains the code to run simulations for the Stochastic SIR Model
"""
# import required packages
import sys
sys.path.append('../')
from sir.stochasticsir import *
import numpy as np 
from numpy.random import randint, rand
import matplotlib.pyplot as plt

# Number of cases during peak of pandemic
# First set of simulations: constant number of contacts per person
trials = 500
ps = [0.1, 0.05]
Rs = [2, 14]
for p in ps:
    for r in Rs:
        simulations = []
        for k in range(trials):            
            result = stochastic_constant_contacts(p, r)
            infected = result[1]
            everinfected = max(infected)
            simulations.append(everinfected)
        plt.hist(simulations)
        plt.xlabel('Maximum Number of Cases')
        plt.ylabel('Frequency')
        plt.title('Stochastic SIR with p = {} and R = {}'.format(p, r))
        plt.show()
        plt.savefig('Stochastic p={} and R={}'.format(p,r))

# # Second set of simulations: fixed number of contacts over time, but randomly chosen for each individual
# trials = 500
# ps = [0.1, 0.05]
# Rs = [2, 14]
# for p in ps:
#     for r in Rs:
#         simulations = []
#         for k in range(trials):            
#             result = stochastic_fixed_contacts(p, r)
#             infected = result[1]
#             everinfected = max(infected)
#             simulations.append(everinfected)
#         plt.hist(simulations)
#         plt.xlabel('Maximum Number of Cases')
#         plt.ylabel('Frequency')
#         plt.title('Stochastic SIR with p = {} and R = {}'.format(p, r))
#         plt.show()

# # Third set of simulations: contacts = fixed component plus random component
# trials = 500
# ps = [0.1, 0.05]
# Rs = [2, 14]
# for p in ps:
#     for r in Rs:
#         simulations = []
#         for k in range(trials):            
#             result = stochastic_random_contacts(p, r)
#             infected = result[1]
#             everinfected = max(infected)
#             simulations.append(everinfected)
#         plt.hist(simulations)
#         plt.xlabel('Maximum Number of Cases')
#         plt.ylabel('Frequency')
#         plt.title('Stochastic SIR with p = {} and R = {}'.format(p, r))
#         plt.show()
        


# for the duration of the pandemic
trials = 500
ps = [0.1, 0.01]
Rs = [14]
for p in ps:
    for r in Rs:
        simulations = []
        for k in range(trials):            
            result = stochastic_constant_contacts(p, r)[3]
            simulations.append(result)
        plt.hist(simulations)
        plt.xlabel('Duration of Pandemic')
        plt.ylabel('Frequency')
        plt.title('Stochastic SIR with p = {} and R = {}'.format(p, r))
        plt.show()
        plt.savefig('Duration for p={} and R={}')