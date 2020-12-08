import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.integrate import odeint

import sys
sys.path.append("../")
from sir.ode_function import *
from sir.ode_function_spatial import *
from scipy.optimize import curve_fit
from lmfit import Parameters, minimize
import random


##Spatial Script - Center
b = .15
k = .10
p = .50
m = 50
C = [b, k, p, m]

L = Laplacian(m)

S_init = np.ones((m,m))
S_init[m//2, m//2] = .99999 #center block start
I_init = np.zeros((m,m))
I_init[m//2, m//2] = .00001 #center block start
R_init = np.zeros((m,m))

S = np.reshape(S_init, (m**2,1))
I = np.reshape(I_init, (m**2,1))
R = np.reshape(R_init, (m**2,1))
SIR_init = np.append(np.append(S,I),R)

tspan = np.linspace(0, 300, 301) #300 days

sol_spatial_middle = solve_ivp(lambda t, SIR: spatial(t, SIR, L, C), \
                [tspan[0], tspan[-1]], SIR_init, t_eval=tspan, vectorized=True)

numtimes = sol_spatial_middle.t.shape[0]
sol_S = sol_spatial_middle.y[:m**2]
sol_I = sol_spatial_middle.y[m**2:2*m**2]
sol_R = sol_spatial_middle.y[2*m**2:]

sol_S_mat = np.reshape(sol_S, (m,m,numtimes)) #turns into m x m grid time sequence in each block
sol_I_mat = np.reshape(sol_I, (m,m,numtimes))
sol_R_mat = np.reshape(sol_R, (m,m,numtimes))

final_R_center = sol_R_mat[:,:,-1] #Total removed at end of our time in a grid format

fig1 = plt.figure()
heatmap2d(final_R_center)
plt.show()
fig1.savefig("Final R Values, Starting in Center, p = .5.png")


##Spatial Script - CORNER

b = .15
k = .10
p = .50
m = 50
C = [b, k, p, m]

L = Laplacian(m)

S_init = np.ones((m,m))
S_init[0, 0] = .99999 #corner start
I_init = np.zeros((m,m))
I_init[0, 0] = .00001 #corner start
R_init = np.zeros((m,m))

S = np.reshape(S_init, (m**2,1))
I = np.reshape(I_init, (m**2,1))
R = np.reshape(R_init, (m**2,1))
SIR_init = np.append(np.append(S,I),R)

tspan = np.linspace(0, 300, 301) #300 days


sol_spatial_corner = solve_ivp(lambda t, SIR: spatial(t, SIR, L, C), \
                [tspan[0], tspan[-1]], SIR_init, t_eval=tspan, vectorized=True)

numtimes = sol_spatial_corner.t.shape[0]
sol_S = sol_spatial_corner.y[:m**2]
sol_I = sol_spatial_corner.y[m**2:2*m**2]
sol_R = sol_spatial_corner.y[2*m**2:]

sol_S_mat = np.reshape(sol_S, (m,m,numtimes)) #turns into m x m grid time sequence in each block
sol_I_mat = np.reshape(sol_I, (m,m,numtimes))
sol_R_mat = np.reshape(sol_R, (m,m,numtimes))

final_R_corner = sol_R_mat[:,:,-1] #Total removed at end of our time in a grid format

fig2 = plt.figure()
heatmap2d(final_R_corner)
plt.show()
fig2.savefig("Final R Values, Starting in Corner, p = .5.png")


##Spatial Script - Random
b = .15
k = .10
p = .50
m = 50
C = [b, k, p, m]

L = Laplacian(m)

S = np.ones((m**2,1))
I = np.zeros((m**2,1))
R = np.zeros((m**2,1))

totals = 0
for i in range(m**2):
    n = random.random()
    if n <.25:
        I[i] = 1
        totals += 1
        
for j in range(m**2):
    if I[j] == 1:
        I[j] == .00001/totals #distrubiting same %of population infected across random grid points
        S[j] == 1 - I[j]
        
SIR_init = np.append(np.append(S,I),R)

tspan = np.linspace(0, 300, 301) #300 days

sol_spatial_random = solve_ivp(lambda t, SIR: spatial(t, SIR, L, C), \
                [tspan[0], tspan[-1]], SIR_init, t_eval=tspan, vectorized=True)

numtimes = sol_spatial_random.t.shape[0]
sol_S = sol_spatial_random.y[:m**2]
sol_I = sol_spatial_random.y[m**2:2*m**2]
sol_R = sol_spatial_random.y[2*m**2:]

sol_S_mat = np.reshape(sol_S, (m,m,numtimes)) #turns into m x m grid time sequence in each block
sol_I_mat = np.reshape(sol_I, (m,m,numtimes))
sol_R_mat = np.reshape(sol_R, (m,m,numtimes))

final_R_random = sol_R_mat[:,:,-1] #Total removed at end of our time in a grid format

fig3 = plt.figure()
heatmap2d(final_R_random)
plt.show()
fig3.savefig("Final R Values, Starting Randomly, p = .5.png")

##Spatial Script - Center
b = .15
k = .10
p = .75
m = 50
C = [b, k, p, m]

L = Laplacian(m)

S_init = np.ones((m,m))
S_init[m//2, m//2] = .99999 #center block start
I_init = np.zeros((m,m))
I_init[m//2, m//2] = .00001 #center block start
R_init = np.zeros((m,m))

S = np.reshape(S_init, (m**2,1))
I = np.reshape(I_init, (m**2,1))
R = np.reshape(R_init, (m**2,1))
SIR_init = np.append(np.append(S,I),R)

tspan = np.linspace(0, 300, 301) #300 days

sol_spatial_middle = solve_ivp(lambda t, SIR: spatial(t, SIR, L, C), \
                [tspan[0], tspan[-1]], SIR_init, t_eval=tspan, vectorized=True)

numtimes = sol_spatial_middle.t.shape[0]
sol_S = sol_spatial_middle.y[:m**2]
sol_I = sol_spatial_middle.y[m**2:2*m**2]
sol_R = sol_spatial_middle.y[2*m**2:]

sol_S_mat = np.reshape(sol_S, (m,m,numtimes)) #turns into m x m grid time sequence in each block
sol_I_mat = np.reshape(sol_I, (m,m,numtimes))
sol_R_mat = np.reshape(sol_R, (m,m,numtimes))

final_R_center = sol_R_mat[:,:,-1] #Total removed at end of our time in a grid format

fig4 = plt.figure()
heatmap2d(final_R_center)
plt.show()
fig4.savefig("Final R Values, Starting in Center, p = .75.png")

##Spatial Script - Center
b = .15
k = .10
p = .25
m = 50
C = [b, k, p, m]

L = Laplacian(m)

S_init = np.ones((m,m))
S_init[m//2, m//2] = .99999 #center block start
I_init = np.zeros((m,m))
I_init[m//2, m//2] = .00001 #center block start
R_init = np.zeros((m,m))

S = np.reshape(S_init, (m**2,1))
I = np.reshape(I_init, (m**2,1))
R = np.reshape(R_init, (m**2,1))
SIR_init = np.append(np.append(S,I),R)

tspan = np.linspace(0, 300, 301) #300 days

sol_spatial_middle = solve_ivp(lambda t, SIR: spatial(t, SIR, L, C), \
                [tspan[0], tspan[-1]], SIR_init, t_eval=tspan, vectorized=True)

numtimes = sol_spatial_middle.t.shape[0]
sol_S = sol_spatial_middle.y[:m**2]
sol_I = sol_spatial_middle.y[m**2:2*m**2]
sol_R = sol_spatial_middle.y[2*m**2:]

sol_S_mat = np.reshape(sol_S, (m,m,numtimes)) #turns into m x m grid time sequence in each block
sol_I_mat = np.reshape(sol_I, (m,m,numtimes))
sol_R_mat = np.reshape(sol_R, (m,m,numtimes))

final_R_center = sol_R_mat[:,:,-1] #Total removed at end of our time in a grid format

fig5 = plt.figure()
heatmap2d(final_R_center)
plt.show()
fig5.savefig("Final R Values, Starting in Center, p = .25.png")