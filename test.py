"""
Implement Unit Tests
"""

import unittest
import numpy as np

# Imports defined functions
import sys
sys.path.append("../")
from sir.ode_function import *
from sir.ode_function_spatial import *
from sir.discretemodel import *
from sir.discretemodelspatial import *
from sir.stochasticsir import *

###########################################################Basic ODE Model########################################################################################
class TestODEs(unittest.TestCase):

    def test_partials_ODE(self):
        '''
        This will test that x dot, y dot, and z dot are sufficiently close to the solution's respective discretized results
        '''
        h = 600  # Time Step - 600 days
        k = 2 * h  # Time Step - half days
        SIR_init = np.array([0.99999, 0.00001, 0])  # Initial Condition
        tspan = np.linspace(0, 600, k + 2)  # 600 days, halfday-steps + 1 extra

        b = .30  # Infection Rate
        k = .20  # Removal Rate
        c = [b, k]  # Array of constants (referenced in derivative function)

        sol = solve_ivp(lambda t, SIR: f(t, SIR, c), \
                        [tspan[0], tspan[-1]], SIR_init, t_eval=tspan)

        x_array = np.array(sol.y[0, :-1])  # Make these np arrays for element-wise subtraction
        y_array = np.array(sol.y[1, :-1])  # Make these np arrays for element-wise subtraction
        z_array = np.array(sol.y[2, :-1])  # Make these np arrays for element-wise subtraction

        derivatives = np.zeros((sol.y.shape[0], sol.y.shape[1] - 1))  # Building Derivatives
        for i in range(sol.y.shape[1] - 1):
            upper = sol.y[:, i + 1]
            lower = sol.y[:, i]
            finite_difference = (upper - lower) / k
            derivatives[0, i] = finite_difference[0]
            derivatives[1, i] = finite_difference[1]
            derivatives[2, i] = finite_difference[2]

        xderivative_array = np.zeros(x_array.shape)
        yderivative_array = np.zeros(y_array.shape)
        zderivative_array = np.zeros(z_array.shape)

        # xdot
        xderivative_array = np.array(derivatives[0, :])  # Finite Differences Derivatives
        x_dot_function = -1 * b * x_array * y_array  # Solution results plugged into differential equation
        xdifference = x_dot_function - xderivative_array  # Difference should be zero

        for i in range(xdifference.shape[0]):  # For all solution points
            self.assertTrue(np.abs(xdifference[i]) < .05)  # Test checks if absolute difference is close enough to 0

        # ydot
        yderivative_array = np.array(derivatives[1, :])  # Finite Differences Derivatives
        y_dot_function = b * x_array * y_array - k * y_array  # Solution results plugged into differential equation
        ydifference = y_dot_function - yderivative_array  # Difference should be zero

        for i in range(ydifference.shape[0]):  # For all solution points
            self.assertTrue(np.abs(ydifference[i]) < .05)  # Test checks if absolute difference is close enough to 0

        # zdot
        zderivative_array = np.array(derivatives[2, :])  # Finite Differences Derivatives
        z_dot_function = k * y_array  # Solution results plugged into differential equation
        zdifference = z_dot_function - zderivative_array  # Difference should be zero

        for i in range(zdifference.shape[0]):  # For all solution points
            self.assertTrue(np.abs(zdifference[i]) < .05)  # Test checks if absolute difference is close enough to 0

    def test_sums(self):
        '''
        This will test that x dot, y dot, and z dot are sufficiently close to the solution's respective discretized results
        '''
        h = 600  # Time Step - days
        k = 2 * h  # Time Step - half days
        SIR_init = np.array([0.99999, 0.00001, 0])  # Initial Condition
        tspan = np.linspace(0, 600, k + 2)  # 600 days, halfday-steps + 1 extra

        b = .30  # Infection Rate
        k = .20  # Removal Rate
        c = [b, k]  # Array of constants (referenced in derivative function)

        sol = solve_ivp(lambda t, SIR: f(t, SIR, c), \
                        [tspan[0], tspan[-1]], SIR_init, t_eval=tspan)

        x_array = np.array(sol.y[0, :-1])  # Make these np arrays for element-wise adddition
        y_array = np.array(sol.y[1, :-1])  # Make these np arrays for element-wise addition
        z_array = np.array(sol.y[2, :-1])  # Make these np arrays for element-wise addition

        sum_array = x_array + y_array + z_array  # This should equal one
        ones = np.ones(sum_array.shape)  # Construct actual ones
        diff = ones - sum_array  # This should be close to zero

        for i in range(diff.shape[0]):
            self.assertTrue(np.abs(diff[i]) < .005)  # We test to see if this is close enough to zero

    def test_derivative_sums(self):
        '''
        This will test that x dot, y dot, and z dot are sufficiently close to the solution's respective discretized results
        '''
        h = 600  # Time Step - days
        k = 2 * h  # Time Step - half days
        SIR_init = np.array([0.99999, 0.00001, 0])  # Initial Condition
        tspan = np.linspace(0, 600, k + 2)  # 600 days, halfday-steps + 1 extra

        b = .30  # Infection Rate
        k = .20  # Removal Rate
        c = [b, k]  # Array of constants (referenced in derivative function)

        sol = solve_ivp(lambda t, SIR: f(t, SIR, c), \
                        [tspan[0], tspan[-1]], SIR_init, t_eval=tspan)

        x_array = np.array(sol.y[0, :-1])  # Make these np arrays for element-wise adddition
        y_array = np.array(sol.y[1, :-1])  # Make these np arrays for element-wise addition
        z_array = np.array(sol.y[2, :-1])  # Make these np arrays for element-wise addition

        derivatives = np.zeros((sol.y.shape[0], sol.y.shape[1] - 1))  # Building Derivatives
        for i in range(sol.y.shape[1] - 1):
            upper = sol.y[:, i + 1]
            lower = sol.y[:, i]
            finite_difference = (upper - lower) / k
            derivatives[0, i] = finite_difference[0]
            derivatives[1, i] = finite_difference[1]
            derivatives[2, i] = finite_difference[2]

        xderivative_array = np.zeros(x_array.shape)
        yderivative_array = np.zeros(y_array.shape)
        zderivative_array = np.zeros(z_array.shape)

        # xdot
        xderivative_array = np.array(derivatives[0, :])  # Finite Differences Derivatives

        # ydot
        yderivative_array = np.array(derivatives[1, :])  # Finite Differences Derivatives

        # zdot
        zderivative_array = np.array(derivatives[2, :])  # Finite Differences Derivatives

        sum_array = xderivative_array + yderivative_array + zderivative_array  # This should be close to zero

        for i in range(sum_array.shape[0]):
            self.assertTrue(np.abs(sum_array[i]) < .005)  # We test to see if this is close enough to zero

########################################################Basic Discrete Model########################################################################################
class TestDiscreteMethod(unittest.TestCase):

    def test_susc(self):
        """
        Tests that Agent class returns susceptible = True
        """
        agent = Agent()
        self.assertEqual(agent.state, 'S')


    def test_inf(self):
        """
        Tests that Agent class returns infected = True
        """
        agent = Agent()
        agent.change_state()
        self.assertEqual(agent.state, 'I')


    def test_rec(self):
        """
        Tests that Agent class returns recovered = True
        """
        agent = Agent()
        agent.change_state()
        agent.change_state()
        self.assertEqual(agent.state, 'R')

    def test_sum(self):
        """
        Tests that S+I+R = N
        """
        bs = [0.1, 0.2, 0.3]
        ks = [0.01, 0.02, 0.03]
        ts = [10, 20, 30]
        ns = [10, 20, 30]

        for b in bs:
            for k in ks:
                for t in ts:
                    for n in ns:
                        counts_sus, counts_inf, counts_rec = run_simulation(b, k, N=n, T=t)
                        for i in range(len(counts_sus)):
                            cts = counts_sus[i] + counts_inf[i] + counts_rec[i]
                            self.assertEqual(cts, n)
    

#############################################################Discrete Spatial Model########################################################################################
class TestDiscreteSpatialMethod(unittest.TestCase):

    def test_change_pos(self):
        """
        Tests the position is within the grid [0,1]x[0,1]
        """
        agent = AgentSpatial()
        for i in range(100):
            agent.change_pos()
            self.assertTrue(0 <= agent.pos[0] <= 1)
            self.assertTrue(0 <= agent.pos[1] <= 1)

    def test_susc(self):
        """
        Tests that Agent class returns 'S'
        """
        agent = AgentSpatial()
        self.assertEqual(agent.state, 'S')

    def test_inf(self):
        """
        Tests that Agent class returns 'I'
        """
        agent = AgentSpatial()
        agent.change_state()
        self.assertEqual(agent.state, 'I')

    def test_rec(self):
        """
        Tests that Agent class returns 'R'
        """
        agent = AgentSpatial()
        agent.change_state()
        agent.change_state()
        self.assertEqual(agent.state, 'R')

    def test_sum(self):
        """
        Tests that S+I+R = N
        """
        qs = [0.1, 0.2, 0.3]
        ks = [0.01, 0.02, 0.03]
        ts = [10, 20, 30]
        ns = [10, 20, 30]
        pos = [False, 'middle', 'corner']

        for q in qs:
            for k in ks:
                for t in ts:
                    for n in ns:
                        for p in pos:
                            counts_sus, counts_inf, counts_rec = discrete_spatial_simulation(k, q, t=t, n=n, position=p)
                            for i in range(len(counts_sus)):
                                cts = counts_sus[i] + counts_inf[i] + counts_rec[i]
                                self.assertEqual(cts, n)

##########################################################Stochastic Binomial SIR Model########################################################################################

class TestStochasticMethod(unittest.TestCase):

    # We use the Agent() class from the discrete model and hence all the tests from there apply here as well
    # Additional tests are defined below

    def test_sum(self):
        """
        Tests that S+I+R = N for the stochastic simulation functions
        """
        ps = [0.1, 0.01, 0.5]
        Rs = [3, 10, 1]
        ns = [10, 20, 30]

        for p in ps:
            for R in Rs:
                for n in ns:
                    counts_sus1, counts_inf1, counts_rec1, t1 = stochastic_constant_contacts(p, R, N=n)
                    counts_sus2, counts_inf2, counts_rec2, t2 = stochastic_fixed_contacts(p, R, N=n)
                    counts_sus3, counts_inf3, counts_rec3, t3 = stochastic_random_contacts(p, R, N=n)
                    for i in range(len(counts_sus1)):
                        cts = counts_sus1[i] + counts_inf1[i] + counts_rec1[i]
                        self.assertEqual(cts, n)
                    for j in range(len(counts_sus2)):
                        cts2 = counts_sus2[j] + counts_inf2[j] + counts_rec2[j]
                        self.assertEqual(cts2, n)
                    for k in range(len(counts_sus3)):
                        cts3 = counts_sus3[k] + counts_inf3[k] + counts_rec3[k]
                        self.assertEqual(cts3, n)
    
    def stop_simulation(self):
        """
        tests that the simulation functions stop immediately after epidemic ends
        """
        ps = [0.1, 0.01, 0.5]
        Rs = [3, 10, 1]
        ns = [10, 20, 30]

        for p in ps:
            for R in Rs:
                for n in ns:
                    counts_sus, counts_inf, counts_rec, t = stochastic_constant_contacts(p, R, N=n)
                    self.assertEqual(counts_inf[-1], 0)
                    self.assertTrue(counts_inf[-2]>0)
    
    def duration(self):
        """
        tests that the function returns the right duration
        """
        ps = [0.1, 0.01, 0.5]
        Rs = [3, 10, 1]
        ns = [10, 20, 30]

        for p in ps:
            for R in Rs:
                for n in ns:
                    counts_sus, counts_inf, counts_rec, t = stochastic_constant_contacts(p, R, N=n)
                    self.assertEqual(len(counts_inf), t)
                    self.assertEqual(len(counts_sus), t)
                    self.assertEqual(len(counts_rec), t)
                    
                    
                    
###########################################################Spatial PDE Model########################################################################################

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
                    
                    
###########################################################Spatial PDE Model########################################################################################

class TestCovidData(unittest.TestCase):
    '''
    Runs the following tests for the ODE case:
    1) Loads the used USA data and checks that x + y + z = 1 for all points of time and gridpoints.
    '''

    def test_sums_covid(self):
        '''
        This will test that x dot, y dot, and z dot are sufficiently close to the solution's respective discretized results
        '''
        #USA Data
        #This curve gives a very long, gradual upswing of a curve (never got virus under control)
        active_cases = np.array([12,12,12,12,12,10,29,29,28,48,51,54,54,57,60,65,85,106,138,200,289,401,504,663,\
                                 949,1248,1638,2228,2828,3693,4763,6677,9811,14561,20454,25474,34922,45503,56757,70075,\
                                 86149,104063,122016,140316,162280,185218,209691,237631,267528,297966,319571,348719,\
                                 379370,407670,437927,468611,493306,515456,537207,561609,580489,599524,627101,645347,\
                                 665654,691029,702928,729268,754691,765060,789001,811827,813185,832278,852657,875838,\
                                 899902,914435,933967,947630,957012,966798,988728,1007474,1014808,1027839,1038210,\
                                 1029294,1034398,1052032,1067067,1076761,1087713,1100086,1111879,1123004,1135703,1108063,\
                                 1113907,1125535,1129540,1130607,1137350,1147488,1161604,1167505,1121306,1123249,\
                                 1113272,1090562,1087883,1096998,1106163,1114747,1121085,1123457,1123067,1137670,\
                                 1138192,1150553,1159882,1160509,1171957,1181252,1197334,1205372,1221266,1240068,\
                                 1248995,1267085,1284853,1313221,1344322,1375121,1404147,1425895,1446302,1477870,\
                                 1509531,1547979,1573649,1591125,1607771,1632979,1657637,1685627,1724281,1757814,\
                                 1789330,1823094,1838566,1864871,1904739,1918750,1948511,1987041,2002696,2033504,\
                                 2049495,2082378,2112416,2146419,2174785,2190324,2205285,2211949,2239980,2269422,\
                                 2293217,2326068,2308193,2327220,2322765,2345677,2368264,2402251,2424853,2423108,\
                                 2436888,2433958,2456144,2483677,2505916,2524912,2516369,2521624,2514642,2526501,\
                                 2544311,2568042,2582334,2571908,2575015,2559795,2571245,2592314,2601160,2619317,\
                                 2626877,2627568,2617839,2613638,2585381,2597276,2610528,2603348,2593561,2578719,\
                                 2583999,2591971,2598579,2607015,2592038,2587499,2576078,2586065,2600044,2610197,\
                                 2617038,2605273,2593627,2581649,2587615,2597264,2596488,2593766,2581452,2585829,\
                                 2574775,2584433,2595507,2603316,2606492,2601291,2604504,2584726,2598878,2619080,\
                                 2646533,2649802,2638901,2647949,2654113,2677929,2673325,2693695,2719305,2732134\
                                 ,2751803,2754282,2778869,2816449,2852166,2884267,2892234,2923089,2948766,2989015,\
                                 3047811,3096373,3130973,3151950,3198518,3249272,3321804,3403276,3476775,3550475,\
                                 3603300,3698377,3794626,3875092,3999921,4089918,4190450,4270311,4361676,4457441,\
                                 4571932,4700526,4787729,4888196,4966711,5054198,5066257,5180990,5250650,5300237,5378205,\
                                 5427502,5499600,5573346,5692947,5828103])
        dates = np.array(["Feb 15","Feb 16","Feb 17","Feb 18","Feb 19","Feb 20","Feb 21",\
                          "Feb 22","Feb 23","Feb 24","Feb 25","Feb 26","Feb 27","Feb 28",\
                          "Feb 29","Mar 01","Mar 02","Mar 03","Mar 04","Mar 05","Mar 06",\
                          "Mar 07","Mar 08","Mar 09","Mar 10","Mar 11","Mar 12","Mar 13",\
                          "Mar 14","Mar 15","Mar 16","Mar 17","Mar 18","Mar 19","Mar 20",\
                          "Mar 21","Mar 22","Mar 23","Mar 24","Mar 25","Mar 26","Mar 27",\
                          "Mar 28","Mar 29","Mar 30","Mar 31","Apr 01","Apr 02","Apr 03",\
                          "Apr 04","Apr 05","Apr 06","Apr 07","Apr 08","Apr 09","Apr 10",\
                          "Apr 11","Apr 12","Apr 13","Apr 14","Apr 15","Apr 16","Apr 17",\
                          "Apr 18","Apr 19","Apr 20","Apr 21","Apr 22","Apr 23","Apr 24",\
                          "Apr 25","Apr 26","Apr 27","Apr 28","Apr 29","Apr 30","May 01",\
                          "May 02","May 03","May 04","May 05","May 06","May 07","May 08",\
                          "May 09","May 10","May 11","May 12","May 13","May 14","May 15",\
                          "May 16","May 17","May 18","May 19","May 20","May 21","May 22",\
                          "May 23","May 24","May 25","May 26","May 27","May 28","May 29",\
                          "May 30","May 31","Jun 01","Jun 02","Jun 03","Jun 04","Jun 05",\
                          "Jun 06","Jun 07","Jun 08","Jun 09","Jun 10","Jun 11","Jun 12",\
                          "Jun 13","Jun 14","Jun 15","Jun 16","Jun 17","Jun 18","Jun 19",\
                          "Jun 20","Jun 21","Jun 22","Jun 23","Jun 24","Jun 25","Jun 26",\
                          "Jun 27","Jun 28","Jun 29","Jun 30","Jul 01","Jul 02","Jul 03",\
                          "Jul 04","Jul 05","Jul 06","Jul 07","Jul 08","Jul 09","Jul 10",\
                          "Jul 11","Jul 12","Jul 13","Jul 14","Jul 15","Jul 16","Jul 17",\
                          "Jul 18","Jul 19","Jul 20","Jul 21","Jul 22","Jul 23","Jul 24",\
                          "Jul 25","Jul 26","Jul 27","Jul 28","Jul 29","Jul 30","Jul 31",\
                          "Aug 01","Aug 02","Aug 03","Aug 04","Aug 05","Aug 06","Aug 07",\
                          "Aug 08","Aug 09","Aug 10","Aug 11","Aug 12","Aug 13","Aug 14",\
                          "Aug 15","Aug 16","Aug 17","Aug 18","Aug 19","Aug 20","Aug 21",\
                          "Aug 22","Aug 23","Aug 24","Aug 25","Aug 26","Aug 27","Aug 28",\
                          "Aug 29","Aug 30","Aug 31","Sep 01","Sep 02","Sep 03","Sep 04",\
                          "Sep 05","Sep 06","Sep 07","Sep 08","Sep 09","Sep 10","Sep 11",\
                          "Sep 12","Sep 13","Sep 14","Sep 15","Sep 16","Sep 17","Sep 18",\
                          "Sep 19","Sep 20","Sep 21","Sep 22","Sep 23","Sep 24","Sep 25",\
                          "Sep 26","Sep 27","Sep 28","Sep 29","Sep 30","Oct 01","Oct 02",\
                          "Oct 03","Oct 04","Oct 05","Oct 06","Oct 07","Oct 08","Oct 09",\
                          "Oct 10","Oct 11","Oct 12","Oct 13","Oct 14","Oct 15","Oct 16",\
                          "Oct 17","Oct 18","Oct 19","Oct 20","Oct 21","Oct 22","Oct 23",\
                          "Oct 24","Oct 25","Oct 26","Oct 27","Oct 28","Oct 29","Oct 30",\
                          "Oct 31","Nov 01","Nov 02","Nov 03","Nov 04","Nov 05","Nov 06",\
                          "Nov 07","Nov 08","Nov 09","Nov 10","Nov 11","Nov 12","Nov 13",\
                          "Nov 14","Nov 15","Nov 16","Nov 17","Nov 18","Nov 19","Nov 20",\
                          "Nov 21","Nov 22","Nov 23","Nov 24","Nov 25","Nov 26","Nov 27",\
                          "Nov 28","Nov 29","Nov 30","Dec 01","Dec 02","Dec 03","Dec 04"])
        new_cases = np.array([0,0,0,0,0,0,20,0,0,18,4,3,0,3,5,7,25,24,34,63,98,116,\
                              106,163,290,307,386,598,651,891,1107,1972,3191,4816,6004,5110,9594,10882,11621,13643,\
                              17916,19088,19314,20132,23743,25798,27374,30709,33086,34565,26179,32455,34964,32967,\
                              34018,34361,30041,26172,27808,29010,31600,30359,33445,28747,25690,29414,26906,31418,31447,\
                              36514,34712,25879,23932,25891,28956,31383,36312,29059,26395,25755,25560,25673,29767,29266,\
                              25615,20295,19442,23761,22689,27849,27707,23580,19585,23927,21098,22591,28870,24868,21677,\
                              19328,19696,19911,21068,23190,25739,23632,20497,19297,22535,20800,23046,25569,23018,19345,\
                              19175,19240,21237,23444,27649,25882,20523,21187,25890,26400,28346,34118,33745,26594,31883,\
                              36534,39083,40748,47971,44075,41270,45946,47090,53173,58513,60495,50867,46909,51691,56845,\
                              63388,62719,73586,63213,59575,66622,67168,73344,74710,76115,64450,66326,63657,68859,73023,\
                              71273,79440,69444,57482,62396,66257,66229,70260,73539,60048,50136,49867,54902,56242,60192,\
                              63954,57364,49291,49739,54974,56299,54655,61690,53449,38663,41076,44190,45586,46164,50968,\
                              45428,33774,41031,40774,45670,46734,50156,42837,35525,38641,42574,41541,45937,53443,43109,\
                              32751,25906,28800,35765,40307,47146,39810,33582,38433,37017,40800,46895,51936,44125,33750,\
                              36814,36101,42087,45797,53982,43585,34141,37403,44496,41213,47754,52381,50685,34253,41445,\
                              44785,49578,57460,61297,54575,42664,46160,51942,59962,66618,72168,58574,52123,59125,63221,\
                              64732,75100,81834,80733,64238,70269,76628,82066,92170,101702,88324,77041,89352,\
                              95168,108613,123982,132984,128002,110318,127569,144972,144542,162463,188188,160424,\
                              146838,162690,161976,176864,192611,204166,175541,151604,174959,177120,183597,161394,\
                              166060,146593,144613,166904,184198,206073,220643,235272])
        cumulative_cases = new_cases
        for i in np.arange(1,new_cases.shape[0],1):
            cumulative_cases[i] += cumulative_cases[i-1] #creates cumulative cases
    
        total_N_US = 331002651
        urban_N_US = 273975139

        start_index_US = 50 #starting on a more exponential part of the curve
        end_index_US = 294

        cumulative_cases_US = cumulative_cases[start_index_US:end_index_US]
        I_US = active_cases[start_index_US:end_index_US]
        S_US = np.ones((I_US.shape)) * total_N_US - cumulative_cases_US #Construct S from removing new cases from Pop
        R_US = np.ones((I_US.shape)) * total_N_US - S_US - I_US #R = N - S - I

        S_US = S_US/total_N_US #turns into proportions adding to 1
        I_US = I_US/total_N_US
        R_US = R_US/total_N_US

        dates_US = dates[start_index_US:end_index_US]
        days_US = np.arange(0,dates_US.shape[0],1) #indexed days
        
        sum_array = S_US + I_US + R_US #This should equal one
        ones = np.ones(sum_array.shape) #Construct actual ones
        diff = ones - sum_array #This should be close to zero
        
        for i in range(diff.shape[0]): 
            self.assertTrue(np.abs(diff[i]) < .005 ) #We test to see if this is close enough to zero
