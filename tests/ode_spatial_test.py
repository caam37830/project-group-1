"""
Implement Spatial ODE Unit Tests
"""

import unittest
import numpy as np
from scipy.integrate import solve_ivp
import sys
sys.path.append("../")
from sir.ode_function import *
from sir.ode_function_spatial import *

class TestSpatialODEs(unittest.TestCase):
    '''
    Runs the following tests for the ODE case:
    1) Checks finite differences Dx, Dy, Dz are approximately equal to \
    our differential equation solution when plugged into our ODE.
    2) Checks that x + y + z = 1 for all points of time and gridpoints.
    '''
    def test_partials_ODE(self):
        '''
        This will test that x dot, y dot, and z dot are sufficiently close to the solution's respective discretized results
        '''
        b = .15
        k = .10
        p = .50
        m = 5
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

        tspan = np.linspace(0, 300, 601) #600 half days

        sol_spatial_middle = solve_ivp(lambda t, SIR: spatial(t, SIR, L, C), \
                                       [tspan[0], tspan[-1]], SIR_init, t_eval=tspan, vectorized=True)    
        
        sol_S = np.array(sol_spatial_middle.y[:m**2,:-1])
        sol_I = np.array(sol_spatial_middle.y[m**2:2*m**2,:-1])
        sol_R = np.array(sol_spatial_middle.y[2*m**2:,:-1])

        derivatives = np.zeros((sol_spatial_middle.y.shape[0],\
                                sol_spatial_middle.y.shape[1] - 1)) #Building Derivatives, cut off last time
        for i in range(sol_spatial_middle.y.shape[1] - 1):
            upper = sol_spatial_middle.y[:,i+1]
            lower = sol_spatial_middle.y[:,i]
            finite_difference = (upper - lower)/.5 #finite difference step size is 1/2 day
            for j in range(sol_spatial_middle.y.shape[0]):
                derivatives[j,i] = finite_difference[j]     
                           
        #sdot
        sderivative_matrix = np.array(derivatives[:m**2,:]) #Finite Differences Derivatives
        s_dot_function = -1*b*sol_S*sol_I + p*L@sol_S #Solution results plugged into differential equation
        sdifference = s_dot_function - sderivative_matrix #Difference should be zero
        
        for i in range(sdifference.shape[0]): #For all time/grid
            for j in range(sdifference.shape[1]):
                self.assertTrue(np.abs(sdifference[i,j]) < .05) #Test checks if absolute difference is close enough to 0
           
        #idot
        iderivative_matrix = np.array(derivatives[m**2:2*m**2,:]) #Finite Differences Derivatives
        i_dot_function = b*sol_S*sol_I - k*sol_I + p*L@sol_I #Solution results plugged into differential equation
        idifference = i_dot_function - iderivative_matrix #Difference should be zero
        
        for i in range(idifference.shape[0]): #For all time/grid
            for j in range(idifference.shape[1]):
                self.assertTrue(np.abs(idifference[i,j]) < .05) #Test checks if absolute difference is close enough to 0
            
        #rdot
        rderivative_matrix = np.array(derivatives[2*m**2:,:]) #Finite Differences Derivatives
        r_dot_function = k*sol_I + p*L@sol_R #Solution results plugged into differential equation
        rdifference = r_dot_function - rderivative_matrix #Difference should be zero
        
        for i in range(rdifference.shape[0]): #For all time/grid
            for j in range(rdifference.shape[1]):
                self.assertTrue(np.abs(rdifference[i,j]) < .05) #Test checks if absolute difference is close enough to 0
            
    def test_sums_pdes(self):
        '''
        This will test that x dot, y dot, and z dot are sufficiently close to the solution's respective discretized results
        '''
        b = .15
        k = .10
        p = .50
        m = 5
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

        tspan = np.linspace(0, 300, 601) #600 half days

        sol_spatial_middle = solve_ivp(lambda t, SIR: spatial(t, SIR, L, C), \
                                       [tspan[0], tspan[-1]], SIR_init, t_eval=tspan, vectorized=True)    
        
        sol_S = np.array(sol_spatial_middle.y[:m**2])
        sol_I = np.array(sol_spatial_middle.y[m**2:2*m**2])
        sol_R = np.array(sol_spatial_middle.y[2*m**2:])
            
        sum_matrix = sol_S + sol_I + sol_R #This should equal one
        ones = np.ones(sum_matrix.shape) #Construct actual ones
        diff = ones - sum_matrix #This should be close to zero

        for i in range(diff.shape[0]):
            for j in range(diff.shape[1]):    
                self.assertTrue(np.abs(diff[i,j]) < .005 ) #We test to see if this is close enough to zero
