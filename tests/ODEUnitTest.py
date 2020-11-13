"""
Implement ODE Unit Tests
"""

import unittest
import numpy as np
from scipy.integrate import solve_ivp

#Imports defined functions
import sys
sys.path.append("../")
from sir.ODE_Function import *


class TestODEs(unittest.TestCase):
                  
    def test_partials_ODE(self):
        '''
        This will test that x dot, y dot, and z dot are sufficiently close to the solution's respective discretized results
        '''
        h = 600 #Time Step - 600 days
        k = 2*h #Time Step - half days
        SIR_init = np.array([0.99999, 0.00001, 0]) #Initial Condition
        tspan = np.linspace(0, 600, k + 2) #600 days, halfday-steps + 1 extra
        
        b = .30 #Infection Rate
        k = .20 #Removal Rate
        c = [b, k] #Array of constants (referenced in derivative function)
        
        sol = solve_ivp(lambda t, SIR: f(t, SIR, c), \
                [tspan[0], tspan[-1]], SIR_init, t_eval=tspan)
               
        x_array = np.array(sol.y[0,:-1]) #Make these np arrays for element-wise subtraction  
        y_array = np.array(sol.y[1,:-1]) #Make these np arrays for element-wise subtraction
        z_array = np.array(sol.y[2,:-1]) #Make these np arrays for element-wise subtraction

        derivatives = np.zeros((sol.y.shape[0],sol.y.shape[1] - 1)) #Building Derivatives
        for i in range(sol.y.shape[1] - 1):
            upper = sol.y[:,i+1]
            lower = sol.y[:,i]
            finite_difference = (upper - lower)/k
            derivatives[0,i] = finite_difference[0]
            derivatives[1,i] = finite_difference[1]
            derivatives[2,i] = finite_difference[2]        
    
        xderivative_array = np.zeros(x_array.shape)
        yderivative_array = np.zeros(y_array.shape)
        zderivative_array = np.zeros(z_array.shape)

        #xdot
        xderivative_array = np.array(derivatives[0,:]) #Finite Differences Derivatives
        x_dot_function = -1 * b * x_array * y_array #Solution results plugged into differential equation
        xdifference = x_dot_function - xderivative_array #Difference should be zero
        
        for i in range(xdifference.shape[0]): #For all solution points
            self.assertTrue(np.abs(xdifference[i]) < .05) #Test checks if absolute difference is close enough to 0
           
        #ydot
        yderivative_array = np.array(derivatives[1,:]) #Finite Differences Derivatives
        y_dot_function = b * x_array * y_array - k * y_array #Solution results plugged into differential equation
        ydifference = y_dot_function - yderivative_array #Difference should be zero
        
        for i in range(ydifference.shape[0]): #For all solution points
            self.assertTrue(np.abs(ydifference[i]) < .05) #Test checks if absolute difference is close enough to 0
            
        #zdot
        zderivative_array = np.array(derivatives[2,:]) #Finite Differences Derivatives
        z_dot_function = k * y_array #Solution results plugged into differential equation
        zdifference = z_dot_function - zderivative_array #Difference should be zero
        
        for i in range(zdifference.shape[0]): #For all solution points
            self.assertTrue(np.abs(zdifference[i]) < .05) #Test checks if absolute difference is close enough to 0    
            
    def test_sums(self):
        '''
        This will test that x dot, y dot, and z dot are sufficiently close to the solution's respective discretized results
        '''
        h = 600 #Time Step - days
        k = 2*h #Time Step - half days
        SIR_init = np.array([0.99999, 0.00001, 0]) #Initial Condition
        tspan = np.linspace(0, 600, k + 2) #600 days, halfday-steps + 1 extra
        
        b = .30 #Infection Rate
        k = .20 #Removal Rate
        c = [b, k] #Array of constants (referenced in derivative function)
        
        sol = solve_ivp(lambda t, SIR: f(t, SIR, c), \
                [tspan[0], tspan[-1]], SIR_init, t_eval=tspan)
        
        x_array = np.array(sol.y[0,:-1]) #Make these np arrays for element-wise adddition  
        y_array = np.array(sol.y[1,:-1]) #Make these np arrays for element-wise addition
        z_array = np.array(sol.y[2,:-1]) #Make these np arrays for element-wise addition
            
        sum_array = x_array + y_array + z_array #This should equal one
        ones = np.ones(sum_array.shape) #Construct actual ones
        diff = ones - sum_array #This should be close to zero
        
        for i in range(diff.shape[0]):
            self.assertTrue(np.abs(diff[i]) < .005 ) #We test to see if this is close enough to zero

    def test_derivative_sums(self): 
        '''
        This will test that x dot, y dot, and z dot are sufficiently close to the solution's respective discretized results
        '''
        h = 600 #Time Step - days
        k = 2*h #Time Step - half days
        SIR_init = np.array([0.99999, 0.00001, 0]) #Initial Condition
        tspan = np.linspace(0, 600, k + 2) #600 days, halfday-steps + 1 extra
        
        b = .30 #Infection Rate
        k = .20 #Removal Rate
        c = [b, k] #Array of constants (referenced in derivative function)
        
        sol = solve_ivp(lambda t, SIR: f(t, SIR, c), \
                [tspan[0], tspan[-1]], SIR_init, t_eval=tspan)
        
        x_array = np.array(sol.y[0,:-1]) #Make these np arrays for element-wise adddition  
        y_array = np.array(sol.y[1,:-1]) #Make these np arrays for element-wise addition
        z_array = np.array(sol.y[2,:-1]) #Make these np arrays for element-wise addition

        derivatives = np.zeros((sol.y.shape[0],sol.y.shape[1] - 1)) #Building Derivatives
        for i in range(sol.y.shape[1] - 1):
            upper = sol.y[:,i+1]
            lower = sol.y[:,i]
            finite_difference = (upper - lower)/k
            derivatives[0,i] = finite_difference[0]
            derivatives[1,i] = finite_difference[1]
            derivatives[2,i] = finite_difference[2]        
    
        xderivative_array = np.zeros(x_array.shape)
        yderivative_array = np.zeros(y_array.shape)
        zderivative_array = np.zeros(z_array.shape)
            
        #xdot
        xderivative_array = np.array(derivatives[0,:]) #Finite Differences Derivatives
        
        #ydot
        yderivative_array = np.array(derivatives[1,:]) #Finite Differences Derivatives

        #zdot
        zderivative_array = np.array(derivatives[2,:]) #Finite Differences Derivatives
        
        sum_array = xderivative_array + yderivative_array + zderivative_array #This should be close to zero
        
        for i in range(sum_array.shape[0]):
            self.assertTrue(np.abs(sum_array[i]) < .005 ) #We test to see if this is close enough to zero
