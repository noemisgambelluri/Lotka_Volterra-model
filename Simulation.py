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
import argparse


# Instantiate the parser
parser = argparse.ArgumentParser(description='Lotka-Volterra parameters usage')

# Optional argument for settings_file. If the user does not specify
# it, a default file will be used
parser.add_argument('settings_file', default='default_settings.ini', nargs='?', help='File for configuration parameters')

# Optional arguments
parser.add_argument('--alpha', type=float, help='A float value for Alpha parameter (prey per capita growth rate)')
parser.add_argument('--beta', type=float, help='A float value for beta parameter (effect of presence of predators on the prey growth rate))')
parser.add_argument('--delta', type=float, help='A float value for delta parameter (effect of the presence of prey on the predator growth rate)')
parser.add_argument('--gamma', type=float, help='A float value for gamma parameter (predators per capita death rate)')
parser.add_argument('--x0', type=float, help='A float value for x0 (initial population of preys)')
parser.add_argument('--y0', type=float, help='A float value for y0 (initial population of predators)')
parser.add_argument('--t_max', type=float, help='A float value for max simulation time')
parser.add_argument('--num_points', type=int, help='A int value for number of time points for Simulation')

# Parse user-prompted parameters
args = parser.parse_args()

# Read default (or given) configuration file.
config = configparser.ConfigParser()
config.read(args.settings_file)

# Get user-prompted parameters if present (different from None) 
# Otherwise use parameters from configuration file if present
# Otherwise use default parameters
params = config['parameters']
alpha = args.alpha if args.alpha else params.getfloat('alpha', 1.1)
beta = args.beta if args.beta else params.getfloat('beta', 0.4)
delta = args.delta if args.delta else params.getfloat('delta', 0.1)
gamma = args.gamma if args.gamma else params.getfloat('gamma', 0.4)
x0 = args.x0 if args.x0 else params.getfloat('x0', 5.0)
y0 = args.y0 if args.y0 else params.getfloat('y0', 15.0)
t_max = args.t_max if args.t_max else params.getfloat('t_max', 100.0)
num_points = args.num_points if args.num_points else params.getint('num_points', 1000)

# Import path parameters
paths = config['paths']
prey_rates_path = paths.get('prey_rates_path', './data/prey_rates.npy')
pred_rates_path = paths.get('pred_rates_path', './data/pred_rates.npy')
time_path = paths.get('time_path', './data/time.npy')
eq_points_path = paths.get('eq_points_path', './data/eq_points.npy')

# Import path result parameters
txt_file_path = config['txt_file_path']
resultsfile_path = txt_file_path.get('results_path', './data/results.npy')

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
plt.savefig('Dynamicplot.png')
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
plt.savefig('Phasespaceplot.png')
plt.show()
