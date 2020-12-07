import matplotlib.pyplot as plt
from networkx.generators.community import stochastic_block_model as sbm
import networkx as nx
import sys
sys.path.append("../")
from sir.spatialextension import *

# Draws an example SBM
ks = [10, 10]
ps = [[1, 0.5], [0.5, 1]]
G = sbm(ks, ps)
nx.draw(G)

# Simulation for write-up
S, I, R, S_agg, I_agg, R_agg, pop = simulation(ks, ps, 0.75, 0.05, 1000, pop_dist=None, inf_dist=None, inf_rate=0.01)
S_c, I_c, R_c = clusterize(ks, S, I, R, pop)

# Corresponding graphs
# Graph 1: SIR
plt.plot(S_agg, label = 'S')
plt.plot(I_agg, label = 'I')
plt.plot(R_agg, label = 'R')
plt.xlabel('t')
plt.ylabel('% of pop')
plt.title('Spatial SIR with SBM spatial model')
plt.legend()
plt.show()

# Graph 2: Cluster S
labels = ['Cluster 1', 'Cluster 2']
[a, b] = plt.plot(S_c)
plt.legend([a, b], labels)
plt.title('Susceptible by Clusters')
plt.xlabel('t')
plt.ylabel('% of population susceptible')

# Graph 3: Cluster I
labels = ['Cluster 1', 'Cluster 2']
[a, b] = plt.plot(I_c)
plt.legend([a, b], labels)
plt.title('Infections by Clusters')
plt.xlabel('t')
plt.ylabel('% of population infected')

# Graph 4: Cluster R
labels = ['Cluster 1', 'Cluster 2']
[a, b] = plt.plot(R_c)
plt.legend([a, b], labels)
plt.title('Recovered by Clusters')
plt.xlabel('t')
plt.ylabel('% of population recovered')

# Get clusters
S_c1 = []
I_c1 = []
R_c1 = []
S_c2 = []
I_c2 = []
R_c2 = []
for i in range(len(S_c)):
    S_c1.append(S_c[i][0])
    I_c1.append(I_c[i][0])
    R_c1.append(R_c[i][0])
    S_c2.append(S_c[i][1])
    I_c2.append(I_c[i][1])
    R_c2.append(R_c[i][1])

# Graph 5: Cluster 1 SIR
plt.plot(S_c1, label='S')
plt.plot(I_c1, label='I')
plt.plot(R_c1, label='R')
plt.xlabel('t')
plt.ylabel('% of pop')
plt.title('Spatial SIR with SBM spatial model, cluster 1')
plt.legend()
plt.show()

# Graph 6: Cluster 2 SIR
plt.plot(S_c2, label='S')
plt.plot(I_c2, label='I')
plt.plot(R_c2, label='R')
plt.xlabel('t')
plt.ylabel('% of pop')
plt.title('Spatial SIR with SBM spatial model, cluster 2')
plt.legend()
plt.show()