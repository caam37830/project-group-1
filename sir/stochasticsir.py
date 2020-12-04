"""
This document contains the code for setting up the stochastic SIR model. 
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

# Simulations to calculate the trajectories of S, I and R people
# First set of simulations: constant number of contacts per person
def stochastic_constant_contacts(p, R, N=200, contacts=4):
    """
    runs simulation of the stochastic SIR model
    """
    pop = [Agent() for i in range(N)]
    pop[0].change_state()
    counts_sus = []
    counts_inf = []
    counts_rec = []
    t_firstinf = np.zeros(N)
    t_firstinf[0] = 0
    t=0
    while count_infected(pop)>0:
        t = t + 1
        inf = count_infected(pop)
        for i in range(N):
            if pop[i].state == 'S':
                contacts_num = contacts
                prob = 1 - (1-((p*inf)/(N-1)))**contacts_num        
                if rand() < prob:
                    pop[i].change_state()
                    t_firstinf[i] = t
            if pop[i].state == 'I':
                if t_firstinf[i] == t-R-1:
                    pop[i].change_state()
        counts_sus.append(count_susc(pop))
        counts_inf.append(count_infected(pop))
        counts_rec.append(count_recovered(pop))
    return counts_sus, counts_inf, counts_rec, t

    
# Second set of simulations: fixed number of contacts over time, but randomly chosen for each individual
def stochastic_fixed_contacts(p, R, N=200, fixed=10):
    """
    runs simulation of the stochastic SIR model
    """
    pop = [Agent() for i in range(N)]
    pop[0].change_state()
    counts_sus = []
    counts_inf = []
    counts_rec = []
    t_firstinf = np.zeros(N)
    t_firstinf[0] = 0
    t=0
    nums = fixed + 1
    contact_list = np.random.randint(nums, size=N)
    while count_infected(pop)>0:
        t = t + 1
        inf = count_infected(pop)
        for i in range(N):
            if pop[i].state == 'S':
                contacts = contact_list[i]
                prob = 1 - (1-((p*inf)/(N-1)))**contacts        
                if rand() < prob:
                    pop[i].change_state()
                    t_firstinf[i] = t
            if pop[i].state == 'I':
                if t_firstinf[i] == t-R-1:
                    pop[i].change_state()
        counts_sus.append(count_susc(pop))
        counts_inf.append(count_infected(pop))
        counts_rec.append(count_recovered(pop))
    return counts_sus, counts_inf, counts_rec, t

# Third set of simulations: contacts = fixed component plus random component
def stochastic_random_contacts(p, R, N=200, fixed=10, random=4):
    """
    runs simulation of the stochastic SIR model
    """
    pop = [Agent() for i in range(N)]
    pop[0].change_state()
    counts_sus = []
    counts_inf = []
    counts_rec = []
    t_firstinf = np.zeros(N)
    t_firstinf[0] = 0
    t=0
    fixed_list = np.random.randint(fixed+1, size=N)
    while count_infected(pop)>0:
        t = t + 1
        var = np.random.randint(random+1, size=N)
        contacts = fixed_list + var
        inf = count_infected(pop)
        for i in range(N):
            if pop[i].state == 'S':
                contacts_num = contacts[i]
                prob = 1 - (1-((p*inf)/(N-1)))**contacts_num        
                if rand() < prob:
                    pop[i].change_state()
                    t_firstinf[i] = t
            if pop[i].state == 'I':
                if t_firstinf[i] == t-R-1:
                    pop[i].change_state()
        counts_sus.append(count_susc(pop))
        counts_inf.append(count_infected(pop))
        counts_rec.append(count_recovered(pop))
    return counts_sus, counts_inf, counts_rec, t



