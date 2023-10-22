########################################################################
# Author: Noemi Sgambelluri
# Date: 15 October, 2023
#
# Lotka-Volterra model (also known as 'Predator-Prey equations)
#
# Aim: To define the functions needed to simulate the Lotka-Volterra model.
#########################################################################

import numpy as np
from scipy.integrate import odeint
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

def LotkaVolterra(variables, time, *parameters):

    """
    This function defines the Lotka-Volterra equations for a two species system.

    Parameters:
        variables : array
            A list containing current population levels of the two interacting species.

        time : array 
            A sequence of time points for which to solve the equations.
            Not used by the function but needed for odeint.

        parameters : array of floats
            Lotka-Volterra model parameters that define the interaction 
            between the species: alpha, beta, delta, gamma.

    Returns:
        Rates of change of both the prey and the predator populations (dxdt, dydt).
    """

    x, y = variables
    alpha, beta, delta, gamma = parameters

    # Mathematical implementation of the Lotka-Volterra equations:
    dxdt = alpha * x - beta * x * y
    dydt = delta * x * y - gamma * y

    return dxdt, dydt

def SolveLotkaVolterra(parameters, initial_conditions, t_max, num_points):

    """
    Numerically solve the Lotka-Volterra equations.

    Parameters:
    parameters : array of floats 
        Lotka-Volterra model parameters: alpha, beta, delta, gamma.

    initial_conditions : array of floats
        Initial populations of prey and predator: x0, y0.

    t_max : float
        Maximum time for simulation.

    num_points : int
        Number of time points for simulation.

    Returns:
    sol : array
        An array containing the prey and predator populations at different time points.
    
    t : array
        An array containing the time points.
    """

    # Create a time vector
    t = np.linspace(0, t_max, num_points)
    # Set initial conditions
    x0, y0 = initial_conditions
    alpha, beta, delta, gamma = parameters

    # Numerically solve the Lotka-Volterra equations
    sol = odeint(LotkaVolterra, [x0, y0], t, args= (alpha, beta, delta, gamma))

    return sol, t

def Equilibria(parameters):

    """
    This function computes the two equilibrium points (steady-states solutions), i.e. the population 
    values at which both the predator and prey populations remain constant over time. 
     

    Parameters
        parameters : array of floats
            Parameters (alpha, beta, delta, gamma) that define the interaction between the species

    Returns:
        Two types of population equilibrium points: Extinction equilibrium point (eq_point1) 
        and Coexistence equilibrium point (eq_point2).
    """

    alpha, beta, delta, gamma = parameters

    # Mathematical definition of the equilibrium points of the Lotka-Volterra equations
    eq_point1 = (0.0, 0.0)
    eq_point2 = (gamma/delta, alpha/beta)

    return eq_point1, eq_point2

def AmplitudeandFrequency(sol, t):

    """
    This function calculates the amplitude and frequency of the oscillations patterns of 
    the Predator and Prey's populations to understand the cyclic nature of the 
    predator-prey interaction.

    Parameters:

        sol : array
            Contains the prey and predator populations over time.
        
        t : array
            Containing the time points
    """

    predator_pop = sol[:, 1]
    prey_pop = sol[:, 0]

    # Identify the peaks in the predators populations data
    predator_peaks, _ = find_peaks(predator_pop)
    # Compute time intervals betweem them
    # Subarray of time points corresponding to the peaks of the predator population
    predator_t_intervals = np.diff(t[predator_peaks])
    # Compute frequency on the mean of all time points corresponding to the peak
    predator_freq = 1 / np.mean(predator_t_intervals)
    # Compute amplitude
    predator_amplitude = np.max(predator_pop) - np.min(predator_pop)

    # Identify the peaks in the preys populations data
    prey_peaks, _ = find_peaks(prey_pop)
    # Compute time intervals between them
    prey_t_intervals = np.diff(t[prey_peaks])
    # Compute frequency on the mean of all time points corresponding to the peak
    prey_freq = 1 / np.mean(prey_t_intervals)
    prey_amplitude = np.max(prey_pop) - np.min(prey_pop)

    return prey_amplitude, prey_freq, predator_amplitude, predator_freq

def LotkaVolterraDynamicsPlot(sol, t_max, num_points):

    """
    Plot Lotka-Volterra equations as a function of time.

    Parameters:
    sol : array
        Contains the prey and predator populations over time.

    t_max : float
        Maximum time for simulation.

    num_points : int
        Number of time points for simulation.
    """

    # Create a time vector
    t = np.linspace(0, t_max, num_points)
    plt.figure(figsize=(8,5))
    plt.plot(t, sol[:, 0], label = 'Preys Population (x)', lw = 2)
    plt.plot(t, sol[:, 1], label = 'Predators Population', lw = 2)

    # Add x-axis and y-axis label and legend
    plt.xlabel('Time')
    plt.ylabel('Population')
    plt.legend()
    plt.show()


def PhaseSpacePlot(initial_conditions, sol, eq_point1, eq_point2):

    """
    Plot the phase space of Lotka-Volterra equations and mark the equilibrium points.

    Parameters:
    initial_conditions : array of floats
        Initial populations of preys and predators.

    sol : array
            contains the prey and predator populations over time.

    eq_point1 : float
        Extinction equilibrium point.

    eq_point2 : float 
        Coexistence equilibrium point.
    """

    x0, y0 = initial_conditions
    # Create a figure for the plot
    plt.figure(figsize=(8,5))

    # Plot the phase space trajectory of the Lotka-Volterra equations
    plt.plot(sol[:, 0], sol[:, 1], label = 'Phase space plot of Lotka-Volterra eq', lw = 2)

    # Highlight the initial condition point in red
    plt.scatter(x0, y0, color = 'red', marker = 'o', label = 'Initial Condition', s = 100)

    # Highlight equilibrium points
    plt.scatter(eq_point1, eq_point2, color = 'green', marker = 'x', label = 'Equilibrium Points', s= 100)

    # Set x-axis and y-axis labels and title
    plt.xlabel('Preys population (x)')
    plt.ylabel('Predators Population (y)')
    plt.legend()
    plt.title('Lotka-Volterra equations in Phase Space')
    plt.show()