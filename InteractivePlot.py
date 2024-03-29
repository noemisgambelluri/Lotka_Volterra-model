########################################################################
# Author: Noemi Sgambelluri
# Date: 29 October, 2023
#
# Lotka-Volterra model interactive plot
#
# Aim: To visualize interactively the Lotka Volterra equations.
#########################################################################

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons
import LotkaVolterraModel as LVM
import configparser
import sys

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

# Save Prey and Predator Population rates of change to variable
prey_rates = solution[:, 0]
pred_rates = solution[:, 1]

def LotkaVolterra(alpha, beta, delta, gamma, x0, y0):
    """
        Lotka-Volterra wrapper function used to interactive plot data 
    """
    parameters = (alpha, beta, delta, gamma)
    initial_conditions = [x0, y0]
    solution, time = LVM.SolveLotkaVolterra(parameters, initial_conditions, t_max, num_points)

    # Extract Pray and Predator Population rates of change to variable
    prey_rates = solution[:, 0]
    pred_rates = solution[:, 1]

    return prey_rates, pred_rates

axis_color = 'lightgoldenrodyellow'

# Create plot figure and get axes
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title("Interactive Lotka-Volterra")


# Adjust the subplots region to leave some space for the sliders and buttons
fig.subplots_adjust(left=0.15, bottom=0.4, right = 0.85, top = 0.95, wspace = 0.2, hspace= 0.2)

# Draw the initial plot
# The 'line' variable is used for modifying the line later
[prey_line] = ax.plot(time, prey_rates, linewidth=1, color='red')
[pred_line] = ax.plot(time, pred_rates, linewidth=1, color='blue')
ax.set_xlim([0, time[-1]])

# Add 4 sliders for tweaking the parameters
# Define an axes area and draw a slider in it
alpha_slider_ax  = fig.add_axes([0.1, 0.25, 0.60, 0.015], facecolor=axis_color)
alpha_slider = Slider(alpha_slider_ax, 'alpha', 0.1, 2.0, valinit=alpha)

beta_slider_ax = fig.add_axes([0.1, 0.2, 0.60, 0.015], facecolor=axis_color)
beta_slider = Slider(beta_slider_ax, 'beta', 0.1, 2.0, valinit=beta)

delta_slider_ax = fig.add_axes([0.1, 0.15, 0.60, 0.015], facecolor=axis_color)
delta_slider = Slider(delta_slider_ax, 'delta', 0.1, 2.0, valinit=delta)

gamma_slider_ax = fig.add_axes([0.1, 0.1, 0.60, 0.015], facecolor=axis_color)
gamma_slider = Slider(gamma_slider_ax, 'gamma', 0.1, 2.0, valinit=gamma)

x0_slider_ax  = fig.add_axes([0.1, 0.05, 0.60, 0.015], facecolor=axis_color)
x0_slider = Slider(x0_slider_ax, 'Prey', 1, 100, valinit=x0, valstep=1)

y0_slider_ax = fig.add_axes([0.1, 0.0, 0.60, 0.015], facecolor=axis_color)
y0_slider = Slider(y0_slider_ax, 'Pred', 1, 100, valinit=y0, valstep=1)

# Define an action for modifying the line when any slider's value changes
def sliders_on_change(val):
    prey_rates, pred_rates = LotkaVolterra(alpha_slider.val, beta_slider.val, delta_slider.val, gamma_slider.val, x0_slider.val, y0_slider.val)
    prey_line.set_ydata(prey_rates)
    pred_line.set_ydata(pred_rates)
    fig.canvas.draw_idle()

alpha_slider.on_changed(sliders_on_change)
beta_slider.on_changed(sliders_on_change)
delta_slider.on_changed(sliders_on_change)
gamma_slider.on_changed(sliders_on_change)
x0_slider.on_changed(sliders_on_change)
y0_slider.on_changed(sliders_on_change)

# Add a set of radio buttons for changing population view
pop_radios_ax = fig.add_axes([0.85, 0.1, 0.1, 0.15], facecolor=axis_color)
pop_radios = RadioButtons(pop_radios_ax, ('Prey', 'Pred', 'Both'), active=2)

def pop_radios_on_clicked(label):
    if label == 'Prey':
        prey_line.set_alpha(1)
        pred_line.set_alpha(0)
    elif label == 'Pred':
        prey_line.set_alpha(0)
        pred_line.set_alpha(1)
    else:
        prey_line.set_alpha(1)
        pred_line.set_alpha(1)

    fig.canvas.draw_idle()

pop_radios.on_clicked(pop_radios_on_clicked)

plt.show()