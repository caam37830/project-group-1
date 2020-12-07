from networkx.generators.community import stochastic_block_model as sbm
import networkx as nx
import numpy as np
import random
import sys
sys.path.append("../")


class SpatialSparse:

    def gen_graph(self, ks, ps):
        """
        Takes list of k clusters and list of lists probabilities ps
        and generates:
            SBM graph G
            Measure Matrix
        """
        self.ks = ks
        self.ps = ps

        # Generate graph G and corresponding adjacency matrix
        self.G = sbm(ks, ps)
        Adj = nx.linalg.adj_matrix(self.G).todense()

        # Create a weight/distance matrix
        self.n = len(self.G) # used throughout, callable
        W = np.empty((self.n, self.n))
        for i in range(self.n):
            for j in range(self.n):
                if Adj[i, j] == 0:
                    W[i, j] = 0
                else:
                    W[i, j] = 1/(1 + np.abs(i-j))

        # Create degree array
        deg = np.sum(W, axis=1)

        # Finally, create measure matrix
        self.M = np.empty((self.n, self.n))
        for i in range(self.n):
            for j in range(self.n):
                self.M[i, j] = W[i, j]/deg[i]

    def laplacian(self, I):
        """
        I is a list of infected at time t
        Returns Laplacian list, where each element is the Laplacian of node i at time t
        """
        laplace = np.empty(self.n)
        for i in range(self.n):
            i_list = []
            count = 0
            for j in range(self.n):
                if self.M[i, j] != 0:
                    i_list.append(self.M[i, j]*abs(I[i]-I[j]))
                    count += 1
            if count != 0:
                laplace[i] = sum(i_list)/count
            else:
                laplace[i] = 0
        return laplace


def simulation(ks, ps, beta, gamma, iters, pop_dist=None, inf_dist=None, inf_rate=0.02):
    """
    Input:
    - ks and ps to generate SBM
    - beta and gamma as beta*S -> I, gamma*I -> R
    - iters to specify number of iterations
    - pop_dist and inf_dist to specify the population and infection distribution, which is otherwise
        generated randomly as a function of k
    - inf_rate to specify the number of people initially infected in each infected region
    Returns:
        List of lists with each community's S, I and R
    """
    # Generate a model object and the corresponding graph
    model = SpatialSparse()
    model.gen_graph(ks, ps)
    n = sum(ks)

    # Generate the population (each element is a normalized population, where pop_i in [0, 1] and sum(pop) = 1
    if pop_dist is None:
        pop = np.empty(n)
        sum_pop = 0
        for i in range(n):
            pop[i] = random.randint(1, n)
            sum_pop += pop[i]
        pop = pop*(1/sum_pop)
    else:
        pop = pop_dist

    S = pop
    I = np.zeros(n)
    R = np.zeros(n)

    # Generate a random infected population, ie. randomly choose communities:
    if inf_dist is None:
        for i in range(n):
            if 3/n > np.random.rand(): # Chosen to infect at least one population (unless we are v unlucky)
                I[i] += inf_rate*S[i] # Infect 2%, can play with either 0.1 or 0.02 as hyperparameter
                S[i] -= inf_rate*S[i]

    # Run the simulation
    # Gives raw counts
    S_raw = [S]
    I_raw = [I]
    R_raw = [R]
    for i in range(iters):
        # S I R
        I_lp = model.laplacian(I)

        # Reversed to ensure correct population counts
        R = R + gamma*I
        I = (1-gamma)*I + beta*(np.multiply(S, I) + np.multiply(S, I_lp))
        S = S - beta*(np.multiply(S, I) + np.multiply(S, I_lp))

        S_raw.append(S)
        I_raw.append(I)
        R_raw.append(R)

    # Aggregated counts
    S_agg = []
    I_agg = []
    R_agg = []
    for i in range(iters):
        S_agg.append(sum(S_raw[i]))
        I_agg.append(sum(I_raw[i]))
        R_agg.append(sum(R_raw[i]))

    return S_raw, I_raw, R_raw, S_agg, I_agg, R_agg, pop


def clusterize(ks, S_raw, I_raw, R_raw, pop):
    """
    Input: Cluster ks and S, I and R raw data
    Return: Clustered S's, I's and R's
    """
    S_cluster = []
    I_cluster = []
    R_cluster = []
    t = len(S_raw)

    for i in range(t):
        index = 0
        S_temp = []
        I_temp = []
        R_temp = []

        for j in ks:
            S_temp.append(sum(S_raw[i][index:j+1]/sum(pop[index:j+1])))
            I_temp.append(sum(I_raw[i][index:j+1]/sum(pop[index:j+1])))
            R_temp.append(sum(R_raw[i][index:j+1]/sum(pop[index:j+1])))
            index += j

        S_cluster.append(S_temp)
        I_cluster.append(I_temp)
        R_cluster.append(R_temp)

    return S_cluster, I_cluster, R_cluster