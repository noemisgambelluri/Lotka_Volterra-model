#=======================================================================
# Author: Noemi Sgambelluri
# Date: 22 October, 2023
#
# Simulation
#
# Aim: To simulate the Lotka-Volterra Model.
#=======================================================================

import configparser
import sys
from Functions import LotkaVolterraModel as LVM
import matplotlib.pyplot as plt


# Read configuration file
config=configparser.ConfigParser()
config.read(sys.argv[1])

# Import model parameters     
alpha = float(config['parameters']['alpha'])                
beta = float(config['parameters']['beta'])
delta = float(config['parameters']['delta'])
gamma = float(config['parameters']['gamma'])
x0 = float(config['parameters']['x0'])
y0 = float(config['parameters']['y0'])
t_max = float(config['parameters']['t_max'])
num_points = int(config['parameters']['num_points'])

# Save single parameters to variable
parameters = (alpha, beta, delta, gamma)

# Save initial conditions to variable
initial_conditions = [x0, y0]

# Numerically solve the Lotka-Volterra equations
solution, time = LVM.SolveLotkaVolterra(parameters, initial_conditions, t_max, num_points)

# plot
plt.plot(time, solution[:, 0])
plt.plot(time, solution[:, 1])
plt.legend()
plt.xlabel('time')

plt.show()

#Equilibria(parameters)
#AmplitudeandFrequency(sol, t)
#LotkaVolterraDynamicsPlot(sol, t_max, num_points)
#PhaseSpacePlot(initial_conditions, sol, eq_point1, eq_point2)

