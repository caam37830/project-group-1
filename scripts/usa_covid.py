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


#USA Data
#This curve gives a very long, gradual upswing of a curve (never got virus under control)
active_cases = np.array([12,12,12,12,12,10,29,29,28,48,51,54,54,57,60,65,85,106,138,200,289,401,504,663,949,1248,1638,2228,2828,3693,4763,6677,9811,14561,20454,25474,34922,45503,56757,70075,86149,104063,122016,140316,162280,185218,209691,237631,267528,297966,319571,348719,379370,407670,437927,468611,493306,515456,537207,561609,580489,599524,627101,645347,665654,691029,702928,729268,754691,765060,789001,811827,813185,832278,852657,875838,899902,914435,933967,947630,957012,966798,988728,1007474,1014808,1027839,1038210,1029294,1034398,1052032,1067067,1076761,1087713,1100086,1111879,1123004,1135703,1108063,1113907,1125535,1129540,1130607,1137350,1147488,1161604,1167505,1121306,1123249,1113272,1090562,1087883,1096998,1106163,1114747,1121085,1123457,1123067,1137670,1138192,1150553,1159882,1160509,1171957,1181252,1197334,1205372,1221266,1240068,1248995,1267085,1284853,1313221,1344322,1375121,1404147,1425895,1446302,1477870,1509531,1547979,1573649,1591125,1607771,1632979,1657637,1685627,1724281,1757814,1789330,1823094,1838566,1864871,1904739,1918750,1948511,1987041,2002696,2033504,2049495,2082378,2112416,2146419,2174785,2190324,2205285,2211949,2239980,2269422,2293217,2326068,2308193,2327220,2322765,2345677,2368264,2402251,2424853,2423108,2436888,2433958,2456144,2483677,2505916,2524912,2516369,2521624,2514642,2526501,2544311,2568042,2582334,2571908,2575015,2559795,2571245,2592314,2601160,2619317,2626877,2627568,2617839,2613638,2585381,2597276,2610528,2603348,2593561,2578719,2583999,2591971,2598579,2607015,2592038,2587499,2576078,2586065,2600044,2610197,2617038,2605273,2593627,2581649,2587615,2597264,2596488,2593766,2581452,2585829,2574775,2584433,2595507,2603316,2606492,2601291,2604504,2584726,2598878,2619080,2646533,2649802,2638901,2647949,2654113,2677929,2673325,2693695,2719305,2732134,2751803,2754282,2778869,2816449,2852166,2884267,2892234,2923089,2948766,2989015,3047811,3096373,3130973,3151950,3198518,3249272,3321804,3403276,3476775,3550475,3603300,3698377,3794626,3875092,3999921,4089918,4190450,4270311,4361676,4457441,4571932,4700526,4787729,4888196,4966711,5054198,5066257,5180990,5250650,5300237,5378205,5427502,5499600,5573346,5692947,5828103])
dates = np.array(["Feb 15","Feb 16","Feb 17","Feb 18","Feb 19","Feb 20","Feb 21","Feb 22","Feb 23","Feb 24","Feb 25","Feb 26","Feb 27","Feb 28","Feb 29","Mar 01","Mar 02","Mar 03","Mar 04","Mar 05","Mar 06","Mar 07","Mar 08","Mar 09","Mar 10","Mar 11","Mar 12","Mar 13","Mar 14","Mar 15","Mar 16","Mar 17","Mar 18","Mar 19","Mar 20","Mar 21","Mar 22","Mar 23","Mar 24","Mar 25","Mar 26","Mar 27","Mar 28","Mar 29","Mar 30","Mar 31","Apr 01","Apr 02","Apr 03","Apr 04","Apr 05","Apr 06","Apr 07","Apr 08","Apr 09","Apr 10","Apr 11","Apr 12","Apr 13","Apr 14","Apr 15","Apr 16","Apr 17","Apr 18","Apr 19","Apr 20","Apr 21","Apr 22","Apr 23","Apr 24","Apr 25","Apr 26","Apr 27","Apr 28","Apr 29","Apr 30","May 01","May 02","May 03","May 04","May 05","May 06","May 07","May 08","May 09","May 10","May 11","May 12","May 13","May 14","May 15","May 16","May 17","May 18","May 19","May 20","May 21","May 22","May 23","May 24","May 25","May 26","May 27","May 28","May 29","May 30","May 31","Jun 01","Jun 02","Jun 03","Jun 04","Jun 05","Jun 06","Jun 07","Jun 08","Jun 09","Jun 10","Jun 11","Jun 12","Jun 13","Jun 14","Jun 15","Jun 16","Jun 17","Jun 18","Jun 19","Jun 20","Jun 21","Jun 22","Jun 23","Jun 24","Jun 25","Jun 26","Jun 27","Jun 28","Jun 29","Jun 30","Jul 01","Jul 02","Jul 03","Jul 04","Jul 05","Jul 06","Jul 07","Jul 08","Jul 09","Jul 10","Jul 11","Jul 12","Jul 13","Jul 14","Jul 15","Jul 16","Jul 17","Jul 18","Jul 19","Jul 20","Jul 21","Jul 22","Jul 23","Jul 24","Jul 25","Jul 26","Jul 27","Jul 28","Jul 29","Jul 30","Jul 31","Aug 01","Aug 02","Aug 03","Aug 04","Aug 05","Aug 06","Aug 07","Aug 08","Aug 09","Aug 10","Aug 11","Aug 12","Aug 13","Aug 14","Aug 15","Aug 16","Aug 17","Aug 18","Aug 19","Aug 20","Aug 21","Aug 22","Aug 23","Aug 24","Aug 25","Aug 26","Aug 27","Aug 28","Aug 29","Aug 30","Aug 31","Sep 01","Sep 02","Sep 03","Sep 04","Sep 05","Sep 06","Sep 07","Sep 08","Sep 09","Sep 10","Sep 11","Sep 12","Sep 13","Sep 14","Sep 15","Sep 16","Sep 17","Sep 18","Sep 19","Sep 20","Sep 21","Sep 22","Sep 23","Sep 24","Sep 25","Sep 26","Sep 27","Sep 28","Sep 29","Sep 30","Oct 01","Oct 02","Oct 03","Oct 04","Oct 05","Oct 06","Oct 07","Oct 08","Oct 09","Oct 10","Oct 11","Oct 12","Oct 13","Oct 14","Oct 15","Oct 16","Oct 17","Oct 18","Oct 19","Oct 20","Oct 21","Oct 22","Oct 23","Oct 24","Oct 25","Oct 26","Oct 27","Oct 28","Oct 29","Oct 30","Oct 31","Nov 01","Nov 02","Nov 03","Nov 04","Nov 05","Nov 06","Nov 07","Nov 08","Nov 09","Nov 10","Nov 11","Nov 12","Nov 13","Nov 14","Nov 15","Nov 16","Nov 17","Nov 18","Nov 19","Nov 20","Nov 21","Nov 22","Nov 23","Nov 24","Nov 25","Nov 26","Nov 27","Nov 28","Nov 29","Nov 30","Dec 01","Dec 02","Dec 03","Dec 04"])
new_cases = np.array([0,0,0,0,0,0,20,0,0,18,4,3,0,3,5,7,25,24,34,63,98,116,106,163,290,307,386,598,651,891,1107,1972,3191,4816,6004,5110,9594,10882,11621,13643,17916,19088,19314,20132,23743,25798,27374,30709,33086,34565,26179,32455,34964,32967,34018,34361,30041,26172,27808,29010,31600,30359,33445,28747,25690,29414,26906,31418,31447,36514,34712,25879,23932,25891,28956,31383,36312,29059,26395,25755,25560,25673,29767,29266,25615,20295,19442,23761,22689,27849,27707,23580,19585,23927,21098,22591,28870,24868,21677,19328,19696,19911,21068,23190,25739,23632,20497,19297,22535,20800,23046,25569,23018,19345,19175,19240,21237,23444,27649,25882,20523,21187,25890,26400,28346,34118,33745,26594,31883,36534,39083,40748,47971,44075,41270,45946,47090,53173,58513,60495,50867,46909,51691,56845,63388,62719,73586,63213,59575,66622,67168,73344,74710,76115,64450,66326,63657,68859,73023,71273,79440,69444,57482,62396,66257,66229,70260,73539,60048,50136,49867,54902,56242,60192,63954,57364,49291,49739,54974,56299,54655,61690,53449,38663,41076,44190,45586,46164,50968,45428,33774,41031,40774,45670,46734,50156,42837,35525,38641,42574,41541,45937,53443,43109,32751,25906,28800,35765,40307,47146,39810,33582,38433,37017,40800,46895,51936,44125,33750,36814,36101,42087,45797,53982,43585,34141,37403,44496,41213,47754,52381,50685,34253,41445,44785,49578,57460,61297,54575,42664,46160,51942,59962,66618,72168,58574,52123,59125,63221,64732,75100,81834,80733,64238,70269,76628,82066,92170,101702,88324,77041,89352,95168,108613,123982,132984,128002,110318,127569,144972,144542,162463,188188,160424,146838,162690,161976,176864,192611,204166,175541,151604,174959,177120,183597,161394,166060,146593,144613,166904,184198,206073,220643,235272])
cumulative_cases = new_cases
for i in np.arange(1,new_cases.shape[0],1):
    cumulative_cases[i] += cumulative_cases[i-1] #creates cumulative cases
    
total_N_US = 331002651 #including both to use as parameters
urban_N_US = 273975139 #including both to use as parameters

start_index_US = 50 #start data somewhere up curve
end_index_US = 294 #end of data

cumulative_cases_US = cumulative_cases[start_index_US:end_index_US]
I_US = active_cases[start_index_US:end_index_US]
S_US = np.ones((I_US.shape)) * total_N_US - cumulative_cases_US #Construct S from removing new cases from Pop
R_US = np.ones((I_US.shape)) * total_N_US - S_US - I_US #R = N - S - I

S_US = S_US/total_N_US #turns into proportions adding to 1
I_US = I_US/total_N_US
R_US = R_US/total_N_US

dates_US = dates[start_index_US:end_index_US]
days_US = np.arange(0,dates_US.shape[0],1) #indexed days

#Covid Fit Script
true_S = np.array(S_US)
true_I = np.array(I_US)
true_R = np.array(R_US)
true_SIR = np.array([true_S, true_I, true_R])

#initial conditions
S_init = true_S[0]
I_init = true_I[0]
R_init = true_R[0]

SIR_init = np.array([S_init, I_init, R_init])

#parameter initial estimates from simulation
b = 0.15 #initial guess
k = 0.1 #initial guess
print("R0 = {}".format(b/k))
params = Parameters()
params.add('b', value=b, min=0) #bounding to be positive
params.add('k', value=k, min=0) #bounding to be positive

#t span definition
tspan = np.linspace(0, 600, 601) #600 days

result = minimize(sol_error, params, args=(SIR_init, tspan, true_SIR), method='leastsq')
result.params #This tells us the fitted b, k in a visual table.  Best Visualized in Jupyter Notebook

true_S = np.array(S_US)
true_I = np.array(I_US)
true_R = np.array(R_US)
true_SIR = np.array([true_S, true_I, true_R])
time_cap = true_S.shape[0]

tspan = np.arange(0,time_cap,1)

sol = odeint(ode_model, SIR_init, tspan, args=(0.03612338,0.02448164)) #adjust these in accordance to the fitted parameters

fig = plt.figure()
plt.plot(tspan, true_I, 'b', label = "Actual I Curve")
plt.plot(tspan, sol[1], 'r', label = "Fitted I Curve")
plt.xlabel("Time (days)")
plt.ylabel("Proportion of Population Susceptible")
plt.title("USA Covid S Fit: R0 = {}".format(0.03612338/0.02448164))
plt.legend()
plt.show()
fig.savefig("USA-Covid S Fit.png")
