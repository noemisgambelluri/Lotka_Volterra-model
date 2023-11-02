#########################################################################
# Author: Noemi Sgambelluri
# Date: 1 November, 2023
#
# Lotka-Volterra animation plot
#
# Aim: To visualize animations of the Lotka-Volterra Model.
#########################################################################

import configparser
import sys
from sys import argv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

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

# Import data and parameters
prey_rates = np.load(prey_rates_path)
pred_rates = np.load(pred_rates_path)
time = np.load(time_path)

# Create Populations dynamic plot
fig, ax = plt.subplots(figsize=(8,5))
fig.suptitle('Preys-Predators in Phase Space')

# Plot predators population rates as a function of preys population rate: phase space plot
line1, = ax.plot(prey_rates, prey_rates, lw = 1)

# Highlight the initial condition point in red
IC_point = ax.scatter(x0, y0, color = 'red', marker = 'o', s = 100)
text = ax.text(20, 14.5, '')
