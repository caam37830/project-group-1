import numpy as np
import random
from scipy.spatial import KDTree


class AgentSpatial:
    """
    This class represents an agent.
    Assume that all agents are susceptible and no one is infected or recovered in the beginning.
    This class provides methods to return the state of an individual and also to change it.
    """

    def __init__(self, p=None):
        self.state = 'S'
        self.pos = np.random.rand(2)
        if p:
            self.p = p
        else:
            self.p = 0.01

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

    def change_pos(self):
        """
        Change position of agent by p
        """
        dpos = np.empty(2)
        dpos[0] = random.choice([-1, 1])*np.random.randn(1)
        dpos[1] = random.choice([-1, 1])*np.random.randn(1)
        dpos = self.p*dpos/np.linalg.norm(dpos)

        if 0 <= self.pos[0] + dpos[0] <= 1 and 0 <= self.pos[1] + dpos[1] <= 1:
            self.pos += dpos
        else:
            pass

    def initial_position(self, position):
        """
        """
        self.pos = position

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


def discrete_spatial_simulation(k, q, p=None, n=1000, t=20, position=False, num_agents=5):
    """
    Runs a spatial SIR simulation given:
        k=rate of recovery, q=radius of infection, p=step_size, n=population, t=time
    Returns number of S, I and R individuals at time t
    """
    pop = [AgentSpatial(p) for i in range(n)] # Generates our population

    if position == 'middle':
        middle = [0.5, 0.5]
        for i in range(num_agents):
            pop[i].change_state()
            pop[i].initial_position(middle)

    elif position == 'corner':
        corner = [0, 0]
        for i in range(num_agents):
            pop[i].change_state()
            pop[i].initial_position(corner)

    else:
        for i in range(num_agents):
            pop[i].change_state()

    counts_sus = [count_susc(pop)]
    counts_inf = [count_infected(pop)]
    counts_rec = [count_recovered(pop)]

    for t in range(t):
        position = []
        for p in pop:
            p.change_pos()
            position.append(p.pos)
        tree = KDTree(position)
        for i in range(n):
            if pop[i].state == 'I':
                inds = tree.query_ball_point(position[i], q)
                for ind in inds:
                    if pop[ind].state == 'S':
                        pop[ind].change_state()
                if np.random.rand() < k:
                    pop[i].change_state()

        counts_sus.append(count_susc(pop))
        counts_inf.append(count_infected(pop))
        counts_rec.append(count_recovered(pop))

    return counts_sus, counts_inf, counts_rec




