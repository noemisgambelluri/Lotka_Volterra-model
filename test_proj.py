import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint 
from Functions.LotkaVolterramodel_functions import LotkaVolterra

#define initial conditions and parameters

variables = [9, 4]

parameters = [1, 1, 1, 1]

#create a time vector
t = np.linspace(0, 50, 1000) #time from 0 to 200 with 1000 time points

#solve the differential equations 
sol = odeint(LotkaVolterra, variables, t, args=(parameters,))

#plot the populations
plt.figure(figsize=(8, 5))
plt.plot(t, sol[:,0], label="Prey (x)")
plt.plot(t, sol[:,1], label="Predator (y)")
plt.xlabel("Time(days)")
plt.ylabel("Population")
plt.title("Lotka-Volterra Predator-Prey Simulation")
plt.legend()

plt.show()

