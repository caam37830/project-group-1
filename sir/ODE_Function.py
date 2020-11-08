#!/usr/bin/env python
# coding: utf-8

# In[3]:


import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp


# In[1]:


#Define derivative function
def f(t, SIR, c):
    dSIRdt = [-1 * c[0] * SIR[0] * SIR[1],# S dot
            c[0] * SIR[0] * SIR[1] - c[1] * SIR[1],# I dot 
            c[1] * SIR[1]] #R dot
    return dSIRdt

def p0(t, SIR): #Defining event to find max point
    ydot = c[0] * SIR[0] * SIR[1] - c[1] * SIR[1]
    return ydot


# In[ ]:




