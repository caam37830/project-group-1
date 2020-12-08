import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.integrate import odeint

#Define derivative function
def f(t, SIR, c):
    '''
    This is our ODE.
    Used Inputs: SIR (1x3 vector associated with [x(t), y(t), z(t)], 
                 c (1x2 vector associated with [b, k]
    Outputs: Derivative at each point in time SIR(t).
    '''
    dSIRdt = [-1 * c[0] * SIR[0] * SIR[1], # S dot
            c[0] * SIR[0] * SIR[1] - c[1] * SIR[1], # I dot 
            c[1] * SIR[1]] #R dot
    return dSIRdt
    
#Event Interpolation Results
def EventPrints(sol):
    """
    This function will print results according to the above defined events
    This prints the max infection rate, the peak time, 
    the pandemic total length, and total number of removals from pandemic
    """
    
    if sol.y_events[0].shape == (0,) and sol.y_events[1].shape == (0,): #Lack of Movement
        print("The infected population had no closed maximum.")
        print("The infected population never returned to zero")
    elif sol.y_events[0].shape == (0,) and sol.y_events[1].shape != (0,): #No peak, immediate infection removal
            totaltime = sol.t_events[1][0]
            totalremoved = sol.y_events[1][0][2] * 100
            print("There was no closed maximum of the infected population")
            print("In total, the pandemic lasted {} days.".format(totaltime))
            print("In the process, {}% of the population had to be 'removed' (recovered or dead)."\
                  .format(totalremoved))
    elif sol.y_events[0].shape != (0,) and sol.y_events[1].shape == (0,): #Catches peak, no found end of pandemic
            maxinfectionpop = sol.y_events[0][0][1] * 100
            maxinfectiontime = sol.t_events[0][0]
            print("At it's max, the infected population constituted {}% of the total population."\
              .format(maxinfectionpop))
            print("From the start, it took {} days to reach this maximum."\
              .format(maxinfectiontime))
            print("The infected population never returned to zero")
    elif sol.y_events[0].shape != (0,) and sol.y_events[1].shape != (0,): #Catches peak & end of pandemic (standard case)
        maxinfectionpop = sol.y_events[0][0][1] * 100
        maxinfectiontime = sol.t_events[0][0]
        peaktoendtime = sol.t_events[1][0] - maxinfectiontime
        totaltime = sol.t_events[1][0]
        totalremoved = sol.y_events[1][0][2] * 100
        print("At it's max, the infected population constituted {}% of the total population."\
              .format(maxinfectionpop))
        print("From the start, it took {} days to reach this maximum."\
              .format(maxinfectiontime))
        print("After the peak of infections, it took {} days to reach the end of the pandemic."\
              .format(peaktoendtime))
        print("In total, the pandemic lasted {} days."\
              .format(totaltime))
        print("In the process, {}% of the population had to be 'removed' (recovered or dead)."\
              .format(totalremoved))

def ode_model(SIR, t, b, k):
    '''
    Updated ODE model to take in b and k as separate arguments
    This is used specifically for the COVID fitting via lmfit scripts
    Inputs: SIR as 3x1 initial conditions, b, k
    Outputs: dSIRdt for ode45/solveivp functions
    '''
    S = SIR[0]
    I = SIR[1]
    R = SIR[2]

    dSIRdt = [-b*S*I,
              b*S*I - k*I,
              k*I]

    return dSIRdt

def ode_solver(tspan, SIR_init, params):
    '''
    ODE Solver for real data
    Inputs: tspan, S, I, R time streams and a 'good' guess of parameters b, k
    Outputs: Solution given a 'good' parameter guess.
    '''
    b = params['b'].value
    k = params['k'].value
    sol = odeint(ode_model, SIR_init, tspan, args=(b,k))
    return sol.T #transpose to turn row-wise S, I, R

def sol_error(params, SIR_init, tspan, true_SIR):
    '''
    Error calculation of true and solved data
    Inputs: tspan, S, I, R time streams and parameter vector c = [b, k]
    '''
    sol = ode_solver(tspan, SIR_init, params)
    
    time_shape = true_SIR.shape[1] #gathers amount of time to compare
    S_error = sol[0,:time_shape] - true_SIR[0]
    I_error = sol[1,:time_shape] - true_SIR[1]
    R_error = sol[2,:time_shape] - true_SIR[2]
    
    sol_error = np.append(S_error, I_error) #appends all for return
    sol_error = np.append(sol_error, R_error) #appends all for return 
    return sol_error 