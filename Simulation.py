#########################################################################
# Author: Noemi Sgambelluri
# Date: 22 October, 2023
#
# Simulation
#
# Aim: To simulate the Lotka-Volterra Model.
#########################################################################

import configparser
import sys
import LotkaVolterraModel as LVM
import matplotlib.pyplot as plt
import numpy as np


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

# Import path parameters
prey_rates_path = config['paths']['prey_rates_path']
pred_rates_path = config['paths']['pred_rates_path']
time_path = config['paths']['time_path']
eq_points_path = config['paths']['eq_points_path']
resultsfile_path = config['txt_file_path']['results_path']

# Save single parameters to variable
parameters = (alpha, beta, delta, gamma)

# Save initial conditions to variable
initial_conditions = [x0, y0]

# Numerically solve the Lotka-Volterra equations
solution, time = LVM.SolveLotkaVolterra(parameters, initial_conditions, t_max, num_points)
# Compute the two equilibrium points (steady-states solutions)
eq_points = LVM.Equilibria(parameters)

# Calculate the amplitude and frequency of the oscillations of Predators and Preys populations
prey_ampl, prey_freq, pred_ampl, pred_freq = LVM.AmplitudeandFrequency(solution, time)

# Save Prey Population rates of change to variable
prey_rates = solution[:, 0]

# Save Predator Population rates of change to variable
pred_rates = solution[:, 1]

# Save prey population rates of change to file
np.save(prey_rates_path, prey_rates)
np.save(pred_rates_path, pred_rates)
np.save(time_path, time)
np.save(eq_points_path, eq_points)

# Save results to txt file 
with open(resultsfile_path, 'w', encoding="utf-8") as resultsfile:
    resultsfile.write('Lotka-Volterra equations equilibrium points (i.e. steady-state solutions):\n')
    resultsfile.write(str(eq_points))
    resultsfile.write('\n\nAmplitude and frequency of Prey Population oscillation pattern:\n')
    resultsfile.write(str(prey_ampl))
    resultsfile.write('\n')
    resultsfile.write(str(prey_freq))
    resultsfile.write('\n\nAmplitude and frequency of Predator Population oscillation pattern:\n')
    resultsfile.write(str(pred_ampl))
    resultsfile.write('\n')
    resultsfile.write(str(pred_freq))
    resultsfile.write('\n\nRates of change of the prey population for each time point:\n')
    resultsfile.write(str(prey_rates))
    resultsfile.write('\n\nRates of change of the predator population for each time point:\n')
    resultsfile.write(str(pred_rates))


# Create Populations dynamic plots
plt.figure(figsize=(8,5))
plt.plot(time, prey_rates, label = 'Preys Population (x)', lw = 2)
plt.plot(time, pred_rates, label = 'Predators Population (y)', linestyle = '--', lw = 2)

# Add x-axis,y-axis, label and legend
plt.xlabel('Time')
plt.ylabel('Population')
plt.legend()
plt.show()

# Create Phase Space plot
plt.figure(figsize=(8,5))

# Create array of differnt values for predators initial condition
y0_values  = np.linspace(1, 10, 10) 

# Solve Lotka Volterra equations for all values in predators initial conditions array
for y0 in y0_values:
    initial_conditions = [x0, y0]
    solution, time = LVM.SolveLotkaVolterra(parameters, initial_conditions, t_max, num_points)
    prey_rates = solution[:, 0]
    pred_rates = solution[:, 1]

    # Plot predators population rates as a function of preys population rate: phase space plot
    plt.plot(prey_rates, pred_rates, label = 'y0 = %d' % y0, lw = 2)

# Highlight the initial condition point in red
plt.scatter(x0, y0, color = 'red', marker = 'o', label = 'Initial Condition', s = 100)

# Highlight equilibrium points
plt.scatter(eq_points[0][0], eq_points[0][1], color = 'green', marker = 'x', label = 'Extinction eq. point', s= 100)
plt.scatter(eq_points[1][0], eq_points[1][1], color = 'blue', marker = 'x', label = 'Coexistence eq. point', s= 100)

# Add x-axis, y-axis, label and legend
plt.xlabel('Preys Population (x)')
plt.ylabel('Predators Population (y)')
plt.legend()
plt.show()
