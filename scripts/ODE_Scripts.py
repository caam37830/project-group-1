#!/usr/bin/env python
# coding: utf-8

# In[8]:


import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

#import sys  
#sys.path.append('**/Git/Serpents-n-Pythons/sir/')  
#from ODE_Function import * #scriptName without .py extension  


# In[9]:


#import sys, os
#__file__ = 'ODE_Scripts.ipynb'
#sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sir'))
#import ODE_Function


# In[34]:


#Define derivative function
def f(t, SIR, c):
    dSIRdt = [-1 * c[0] * SIR[0] * SIR[1],# S dot
            c[0] * SIR[0] * SIR[1] - c[1] * SIR[1],# I dot 
            c[1] * SIR[1]] #R dot
    return dSIRdt

def p0(t, SIR): #Defining event to find max point
    ydot = c[0] * SIR[0] * SIR[1] - c[1] * SIR[1]
    return ydot


# In[35]:


#Define time span, initial conditions, and constants
tspan = np.linspace(0, 300, 301) #Time period - 300 days (301 including 0)

SIR_init = [0.99999, 0.00001, 0] #Initial conditions - .001 % of population

b = .30 #Infection Rate
k = .20 #Removal Rate

c = [b, k] #Array of constants (referenced in derivative function)

print("The infection rate parameter is set as {}.".format(b))
print("The removal rate parameter is set as {}.".format(k))
print("The basic reproduction number is hence calculated as {}".format(b/k))


# In[36]:


#Solve differential equation
sol = solve_ivp(lambda t, SIR: f(t, SIR, c),                 [tspan[0], tspan[-1]], SIR_init, t_eval=tspan, events=p0)


# In[37]:


Susceptible = plt.plot(sol.t, sol.y[0], 'r', label='Susceptible')
Infected = plt.plot(sol.t, sol.y[1], 'g', label='Infected')
Removed = plt.plot(sol.t, sol.y[2], 'b', label='Removed')
plt.xlabel('Time (Days)')
plt.ylabel('Proportion of Population')
plt.title('SIR Model')
plt.legend()
plt.show


# In[43]:


#Max Infection Results (Event Interpolation)
print("At it's max, the infected population constituted {}% of the total population."      .format(sol.y_events[0][0][1] * 100))
print("From the start, it took {} days to reach this maximum."      .format(sol.t_events[0][0]))


# In[39]:


#Max Infection Results (Actual Plotted Points)
maxinfectionvalue = np.max(sol.y[1]) #Max infected value
maxinfectionpercent = maxinfectionvalue * 100 #Scales into a percentage of population
maxinfectionday = np.argmax(sol.y[1]) #Finds day # of this result

print("At it's max, the infected population constituted {}% of the total population."      .format(maxinfectionpercent) )
print("From the start, it took {} days to reach this maximum."      .format(sol.t[maxinfectionday]))


# In[17]:


#End of Pandemic Results
postpeak = sol.y[1,maxinfectionday:] #We will be looking at behavior after the peak

endtol = SIR_init[1] #Setting the end of the pandemic tolerance point as the original starting place.

peaktoend = np.argmax(postpeak < endtol) #Finds the post-peak day number of the first value under this tolerance
begintoend = maxinfectionday + peaktoend #Calculates total pandemic time frame
endremoved = sol.y[2,begintoend] * 100 #Returns removed % of population at end of pandemic

print("After the peak of infections, it took {} days to reach the end of the pandemic."      .format(peaktoend))
print("In total, the pandemic lasted {} days."      .format(begintoend))
print("In the process, {}% of the population had to be 'removed' (recovered or dead)."      .format(endremoved))


# In[51]:


#Define time span, initial conditions, and constants
tspan = np.linspace(0, 300, 301) #Time period - 300 days (301 including 0)

SIR_init = [0.99999, 0.00001, 0] #Initial conditions - .001 % of population

brange = np.arange(.05, .55, .05) #infection rates
krange = np.arange(.05, .55, .05) #removal rates

for b in brange:
    for k in krange:
        c = [b, k]
        r0 = b/k
        
        #Solve differential equation
        sol = solve_ivp(lambda t, SIR: f(t, SIR, c),                         [tspan[0], tspan[-1]], SIR_init, t_eval=tspan, events=p0)
        
        figname = 'figure' + str(b) + "_" + str(k)
        plt.plot(sol.t, sol.y[0], 'r', label='Susceptible')
        plt.plot(sol.t, sol.y[1], 'g', label='Infected')
        plt.plot(sol.t, sol.y[2], 'b', label='Removed')
        plt.xlabel('Time (Days)')
        plt.ylabel('Proportion of Population')
        plt.title('SIR Model, b = {}, k = {}, r0 = {}'.format(b, k, r0))
        plt.legend()
        plt.show()
        

        #Max Infection Results (Actual Plotted Points)
        maxinfectionvalue = np.max(sol.y[1]) #Max infected value
        maxinfectionpercent = maxinfectionvalue * 100 #Scales into a percentage of population
        maxinfectionday = np.argmax(sol.y[1]) #Finds day # of this result

        print("At it's max, the infected population constituted {}% of the total population."              .format(maxinfectionpercent) )
        print("From the start, it took {} days to reach this maximum."              .format(sol.t[maxinfectionday]))
        
        #End of Pandemic Results
        postpeak = sol.y[1,maxinfectionday:] #We will be looking at behavior after the peak

        endtol = SIR_init[1] #Setting the end of the pandemic tolerance point as the original starting place.

        peaktoend = np.argmax(postpeak < endtol) #Finds the post-peak day number of the first value under this tolerance
        begintoend = maxinfectionday + peaktoend #Calculates total pandemic time frame
        endremoved = sol.y[2,begintoend] * 100 #Returns removed % of population at end of pandemic

        print("After the peak of infections, it took {} days to reach the end of the pandemic."              .format(peaktoend))
        print("In total, the pandemic lasted {} days."              .format(begintoend))
        print("In the process, {}% of the population had to be 'removed' (recovered or dead)."              .format(endremoved))
plt.show()      


# In[50]:


plt.show()


# In[ ]:




