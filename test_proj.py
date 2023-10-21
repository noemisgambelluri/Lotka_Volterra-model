import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint 
from Functions.LotkaVolterramodel_functions import LotkaVolterra

#define the Lotka-Volterra parameters
alpha = 1
beta = 1
delta = 1
gamma = 1

#create an array of time values
time_values = np.linspace(0, 200, 1000) 

#create an array of different initial conditions
IC = np.linspace(1.0, 7.0, 10)

#Create a fiure for the Lotka Volterra equations as a function of time
plt.figure(figsize=(8, 5))
for initial_conditions in IC:
    sol = odeint(LotkaVolterra, IC, time_values, args = (alpha, beta, delta, gamma))
    plt.plot(time_values, sol[:, 0], label = "Preys", lw = 1)
    plt.plot(time_values, sol[:, 1], label = 'Predators', lw = 1, linestyle = '--')

plt.xlabel("Time")
plt.ylabel("Population")
plt.title("Lotka-Volterra equations equations as a function of Time")
plt.legend()
plt.show()

