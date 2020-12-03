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
        self.state = 'S'

    def state(self):
        """
        returns if person is S, I or R
        """
        return self.state
    
    def change_state(self):
        """
        Changes state from S to I, or I to R
        """
        if self.state == 'S':
            self.state = 'I'
        elif self.state == 'I':
            self.state = 'R'
        else:
            pass

# functions to count the number of infected, recovered and susceptible at a given point in time
def count_susc(pop):
    """
    Returns # of susceptible people
    """
    return sum(p.state == 'S' for p in pop)


def count_infected(pop):
    """
    Returns # of infected people
    """
    return sum(p.state == 'I' for p in pop)


def count_recovered(pop):
    """
    Returns # of recovered people
    """
    return sum(p.state == 'R' for p in pop)


# function to run a simulation to return the trends in S, I and R
def run_simulation(b, k, N=1_000, T=20):
    """
    return the number of people S, I and R for each time period t
    """    
    pop = [Agent() for i in range(N)] # Generates our population
    pop[0].change_state() # Creates patient zero
    counts_sus = [count_susc(pop)]
    counts_inf = [count_infected(pop)]
    counts_rec = [count_recovered(pop)]
    for t in range(T):
    # update the population
        for i in range(N):
            if pop[i].state == 'I': # if infected, then infect other susceptible people with p(infect) = b
                for j in range(N):
                    if pop[j].state == 'S':
                        if rand() < b:
                            pop[j].change_state()
                if rand() < k: # if infected, recover with p(recover) = k
                    pop[i].change_state()
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
    pop[0].change_state()
    for t in range(T):
    # update the population
        for i in range(N):
            if pop[i].state == 'I':
                for j in range(N):
                    if pop[j].state == 'S':
                        if rand() < b:
                            pop[j].change_state()
                if rand() < k:
                    pop[i].change_state()
    return count_infected(pop)