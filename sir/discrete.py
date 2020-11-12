"""
This document contains the code for setting up the discrete agent model of disease spread. 
"""

from numpy.random import randint, rand
import numpy as np 

class Agent():
    """
    This class represents an agent. 
    Assume that all agents are susceptible and no one is infected or recovered in the beginning.
    This class provides methods to return the state of an individual and also to change it. 
    """
    
    def __init__(self):
        self.infected = False # if infected = True, the person has been infected
        self.recovered = False # if recovered = True, the person has been recovered
        self.susceptible = True # if susceptible = False, the person has either been infected or has recovered
   
    def is_infected(self):
        """
        returns true if the person is infected
        """
        return self.infected
    
    def is_recovered(self):
        """
        returns true if the person is recovered
        """
        return self.recovered

    def is_susceptible(self):
        """
        returns true if the person is susceptible
        """
        return self.susceptible

    
    def infect(self):
        """
        the person becomes infected
        """
        self.infected = True
        self.susceptible = False
        self.recovered = False

    def recover(self):
        """
        the person recovers
        """
        self.recovered = True
        self.infected = False
        self.susceptible = False


# functions to count the number of infected, recovered and susceptible at a given point in time
def count_infected(pop):
    return sum(p.is_infected() for p in pop)

def count_recovered(pop):
    return sum(p.is_recovered() for p in pop)

def count_susc(pop):
    return sum(p.is_susceptible() for p in pop)


# function to run a simulation to return the trends in S, I and R
def run_simulation(b, k, N=1_000, T=20):
    """
    return the number of people S, I and R for each time period t
    """    
    pop = [Agent() for i in range(N)] # our population
    pop[0].infect()
    counts_sus = [count_susc(pop)]
    counts_inf = [count_infected(pop)]
    counts_rec = [count_recovered(pop)]
    for t in range(T):
    # update the population
        for i in range(N):
            if pop[i].is_infected():
                for j in range(N):
                    if pop[j].is_susceptible():
                        if rand() < b:
                            pop[j].infect()        
                if rand() < k:
                    pop[i].recover()   
        counts_sus.append(count_susc(pop))
        counts_inf.append(count_infected(pop))
        counts_rec.append(count_recovered(pop))

    return counts_sus, counts_inf, counts_rec


# function to construct phase diagram
def run_simulation_phase(b, k, N=1_000, T=10):
    """
    return the number of people infected at time T
    """
    pop = [Agent() for i in range(N)] # our population
    pop[0].infect()
    for t in range(T):
    # update the population
        for i in range(N):
            if pop[i].is_infected():
                for j in range(N):
                    if pop[j].is_susceptible():
                        if rand() < b:
                            pop[j].infect()        
                if rand() < k:
                    pop[i].recover()  
    return count_infected(pop)




    # class simulate(Agent):
#     """
#     runs simulations of the discrete SIR model
#     N is the population size
#     b is the number of interactions each day that could spread the disease (per individual)
#     k is the fraction of the infectious population which recovers each day
#     """

#     def __init__(self, b, k, T=None, N=None):
#         self.b = b
#         self.k = k
#         if N:
#             self.N = N
#         else:
#             self.N = 1000
#         self.pop = [Agent() for i in range(self.N)]
#         if T:
#             self.T = int(T)
#         else:
#             self.T = int(100)

#     def count_infected(self):
#         return sum(p.is_infected() for p in self.pop)

#     def count_recovered(self):
#         return sum(p.is_recovered() for p in self.pop)

#     def count_susc(self):
#         return sum(p.is_susceptible() for p in self.pop)

#     def run_simulation(self):
#         """
#         return the number of susceptible, infected, and recovered people at time T
#         """
#         self.pop[0].infect()
    
#         for t in range(self.T):
#             for i in range(self.N):
#                 if self.pop[i].is_infected():
#                     for j in range(self.N):
#                         if self.pop[j].is_susceptible():
#                             if rand() < self.b:
#                                 self.pop[j].infect()        
#                     if rand() < self.k:
#                         self.pop[i].recover()
#         self.susc = self.count_susc()
#         self.inf =  self.count_infected()
#         self.rec = self.count_recovered()
#         self.cts = [self.susc, self.inf, self.rec]
#         return self.cts 