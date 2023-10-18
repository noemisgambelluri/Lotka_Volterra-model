import numpy as np
import matplotlib 
matplotlib.use('tkagg')
import matplotlib.pyplot as plt
from scipy.integrate import odeint 
from Functions.function_test import LotkaVolterra

#define initial conditions and parameters

variables = [40, 9]

alpha = 0.1
beta = 0.02
delta = 0.3
gamma = 0.01

parameters = [alpha, beta, delta, gamma]

#create a time vector
t = np.linspace(0, 200, 1000) #time from 0 to 200 with 1000 time points

#solve the differential equations 
sol = odeint(LotkaVolterra, variables, t, args=(parameters,))

#plot the populations

