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
ps = [0.1, 0.05] # chose values that are interesting after testing multiple combinations
Rs = [2, 14]
for p in ps:
    for r in Rs:
        simulations = []
        for k in range(trials): # running 500 simulations           
            result = stochastic_constant_contacts(p, r) 
            infected = result[1]
            maximum = max(infected) # get the peak of the pandemic for each simulation
            simulations.append(maximum)
        plt.hist(simulations) # plot the distribution
        plt.xlabel('Maximum Number of Cases')
        plt.ylabel('Frequency')
        plt.title('Stochastic SIR with p = {} and R = {}'.format(p, r))
        plt.show()
        plt.savefig('Stochastic p={} and R={}'.format(p,r) + '.png')
        plt.clf()

# We also performed the simulations below but have not included the results in the final analysis.
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
        for k in range(trials): # 500 simulations           
            result = stochastic_constant_contacts(p, r)[3] # gives the final time the pandemic ends
            simulations.append(result)
        plt.hist(simulations) # plot the distribution of the duration
        plt.xlabel('Duration of Pandemic')
        plt.ylabel('Frequency')
        plt.title('Stochastic SIR with p = {} and R = {}'.format(p, r))
        plt.show()
        plt.savefig('Duration for p={} and R={}.png'.format(p,r))
        plt.clf()

# Comparing the effect of number of contacts for different recovery times
# For peak of pandemic
trials = 500
p=0.1
contacts = [i for i in range(1,11)] # number of contacts for each person
Rs = [1,2,3,4]
for R in Rs:
    mean_infected = [0] # create list containing means for each number of contacts
    for i in contacts:
        simulations = []
        for k in range(trials):            
            result = stochastic_constant_contacts(p, R, contacts=i)[1]
            Maximum = max(result)
            simulations.append(Maximum) # get the peak of the pandemic
        mean = np.mean(simulations)
        mean_infected.append(mean) # get the mean for each R and each number of contacts
    plt.plot(mean_infected, label='R={}'.format(R), marker='o') # plot for each R
plt.xlabel('Number of Contacts')
plt.ylabel('Mean Cases')
plt.legend()
plt.title('Mean Cases During Peak of Pandemic')
plt.show()
plt.savefig('mean_peaks.png')
plt.clf()


# for duration
# code very similar to the one above
trials = 500
p=0.1
contacts = [i for i in range(1,11)]
Rs = [1,2,3,4]
for R in Rs:
    mean_infected = [0]
    for i in contacts:
        simulations = []
        for k in range(trials):            
            result = stochastic_constant_contacts(p, R, contacts=i)[3]
            simulations.append(result)
        mean = np.mean(simulations)
        mean_infected.append(mean)
    plt.plot(mean_infected, label='R={}'.format(R), marker='o')
plt.xlabel('Number of Contacts')
plt.ylabel('Mean Duration')
plt.legend()
plt.title('Mean Duration of Pandemic for Different # Contacts')
plt.show()
plt.savefig('mean_durations.png')
plt.clf()

