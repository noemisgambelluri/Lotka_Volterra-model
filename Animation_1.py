#########################################################################
# Author: Noemi Sgambelluri
# Date: 30 October, 2023
#
# Lotka-Volterra animation plot
#
# Aim: To visualize animations of the Lotka-Volterra Model.
#########################################################################

import configparser
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

if len(sys.argv) < 2:
    settings_file = 'default_settings.ini'
else:
    settings_file = sys.argv[1]

# Read configuration file
config=configparser.ConfigParser()
config.read(settings_file)

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
fig.suptitle('Prey-Predator Populations change rates')

# Plot preys and predators on different lines
line1, = ax.plot(time, pred_rates, label = 'Preys', lw = 2)
line2, = ax.plot(time, prey_rates, label = 'Predators', linestyle = '--', lw = 2)

# Create animation
animation_speed = 3     #speed up animation x3 (change according to your taste)
def animate(i):

    i = i * animation_speed
    line1.set_data(time[:i], pred_rates[:i])
    line2.set_data(time[:i], prey_rates[:i])

    return line1, line2

animation = FuncAnimation(fig, animate, frames=int(num_points/animation_speed), interval=1, repeat=False)

# Add x-axis, y-axis, label and legend
plt.xlabel('Time')
plt.ylabel('Population')
plt.legend()
plt.show()

# Save animation
writer = PillowWriter (fps = num_points)
animation.save('Prey_pred_animation.gif', writer = writer)
