## This script contains code to implement/analyze the continous SIR ODE model


import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

import sys
sys.path.append("../")
from sir.ode_function import *


#Define max infection event
def p0(t, SIR):
    '''
    Defining event to find max point.
    
    Based on our initial conditions, y' will be positive to start,
    and then will reach a max when y' = zero,
    and then it will be negative.
    '''
    ydot = c[0] * SIR[0] * SIR[1] - c[1] * SIR[1]
    return ydot

#Define infection-zero event
def y0(t, SIR): 
    '''
    Defining event to find zero point.
    
    Effectively we want to know when y(t) is sufficiently low enough
    We subtract a value less than the initial condition y0 for the desired return zero
    This is set because we never actually reach a zero.  We only approach it over time.
    '''
    if t==0:
        return 1
    else:
        return SIR[1] - 0.0000095

    
#Single Solution Script

#Define time span, initial conditions, and constants
tspan = np.linspace(0, 600, 601) #Time period - 600 days (601 including 0)

SIR_init = [0.99999, 0.00001, 0] #Initial conditions - .001 % of population

b = .30 #Infection Rate
k = .20 #Removal Rate
r0 = b/k

c = [b, k] #Array of constants (referenced in derivative function)

#Solve differential equation - single solution
sol = solve_ivp(lambda t, SIR: f(t, SIR, c), \
                [tspan[0], tspan[-1]], SIR_init, t_eval=tspan, events=(p0, y0))

Susceptible = plt.plot(sol.t, sol.y[0], 'r', label='Susceptible')
Infected = plt.plot(sol.t, sol.y[1], 'g', label='Infected')
Removed = plt.plot(sol.t, sol.y[2], 'b', label='Removed')
plt.xlabel('Time (Days)')
plt.ylabel('Proportion of Population')
plt.title('SIR Model')
plt.legend()
plt.show

EventPrints(sol)

#Multi Solution Script

#Define time span, initial conditions, and constants
tspan = np.linspace(0, 600, 601) #Time period - 300 days (301 including 0)

SIR_init = [0.99999, 0.00001, 0] #Initial conditions - .001 % of population

parameters = np.array([[0.10, 0.20, 0.30, 0.40, 0.20],\
                       [0.10, 0.15, 0.05, 0.20 ,0.10]])

for i in range(parameters.shape[1]):
    b = parameters[0,i]
    k = parameters[1,i]
    c = [b, k]
    r0 = b/k
        
    #Solve differential equation
    sol = solve_ivp(lambda t, SIR: f(t, SIR, c), \
                    [tspan[0], tspan[-1]], SIR_init, t_eval=tspan, events=(p0,y0))
        
    figure = plt.figure()
    plt.plot(sol.t, sol.y[0], 'r', label='Susceptible')
    plt.plot(sol.t, sol.y[1], 'g', label='Infected')
    plt.plot(sol.t, sol.y[2], 'b', label='Removed')
    plt.xlabel('Time (Days)')
    plt.ylabel('Proportion of Population')
    plt.title('SIR Model, b = {}, k = {}, r0 = {}'.format(b, k, r0))
    plt.legend()
    plt.show()
    figure.savefig('SIR Model, b = {}, k = {}, r0 = {}.png'.format(b, k, r0))
        

    #Event Interpolation Results
    EventPrints(sol)
#Phase Diagram Script

#Define time span, initial conditions, and constants
tspan = np.linspace(0, 600, 601)

SIR_init = [0.99999, 0.00001, 0] 

brange = np.arange(.01, .5, .01) 
krange = np.arange(.01, .5, .01) 

#Initialize tri-criteria arrays
lowrangeb = np.array([])
lowrangek = np.array([])

midrangeb = np.array([])
midrangek = np.array([])

highrangeb = np.array([])
highrangek = np.array([])

#Loop over parametric range
for b in brange:
    for k in krange:
        c = [b, k]
        r0 = b/k
        
        #Solve differential equation
        sol = solve_ivp(lambda t, SIR: f(t, SIR, c), \
                        [tspan[0], tspan[-1]], SIR_init, t_eval=tspan)
        
        #Define qualifying condition
        condition = sol.y[2, -1] #final value of removed individuals
        
        if condition < .05: #very few removed
            lowrangeb = np.append(lowrangeb, np.array([b]), axis = 0)
            lowrangek = np.append(lowrangek, np.array([k]), axis = 0)
        elif condition > .95: #almost all removed
            highrangeb = np.append(highrangeb, np.array([b]), axis = 0)
            highrangek = np.append(highrangek, np.array([k]), axis = 0)
        else: #in the middle
            midrangeb = np.append(midrangeb, np.array([b]), axis = 0)  
            midrangek = np.append(midrangek, np.array([k]), axis = 0)  
            
            
#Plot Phase Diagram From Above Script
Phase_Diagram = plt.figure()
plt.plot(lowrangeb, lowrangek, 'ro', label='Less than 5% Removed')
plt.plot(midrangeb, midrangek, 'bo', label='Between 5% and 95% Removed')
plt.plot(highrangeb, highrangek, 'go', label='Greater than 95% Removed')
plt.xlabel('Infection Rate (b)')
plt.xticks([0.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50])
plt.ylabel('Removal Rate (k)')
plt.yticks([0.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50])
plt.title('Phase Diagram of SIR Behavior with Various b, k')
plt.legend()
plt.show()
Phase_Diagram.savefig('ODE Phase Diagram.png')

