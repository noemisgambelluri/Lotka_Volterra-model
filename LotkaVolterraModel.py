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
    eq_point1 = [0.0, 0.0]
    eq_point2 = [gamma/delta, alpha/beta]

    return eq_point1, eq_point2

def AmplitudeandFrequency(sol, t):

    """
    This main function:
    1. Extracts predator and prey populations from the solution array 
    2. Calls the inner function Ampl_Freq_population for both predator and prey populations 
    3. Returns the calculated amplitude and frequency of the oscillations patterns of 
    the Predator and Prey's populations to understand the cyclic nature of the 
    predator-prey interaction.

    Parameters:

        sol : array
            Contains the prey and predator populations over time.
        
        t : array
            Containing the time points
    Returns:

        prey_amplitude : float
            prey population's oscillation pattern amplitude
        
        prey_freq : float
            prey population's oscillation pattern frequency

        predator_amplitude : float
            predator population's oscillation pattern amplitude

        predator_freq : float
            predator population's oscillation pattern frequency

    """

    def Ampl_Freq_population(time, population):

        """
        This inner function computes amplitude and frequency for each population to be called.
        """

        # Identify the peaks in the populations data
        peaks, _ = find_peaks(population)
        # Compute time intervals between them
        t_intervals = np.diff(t[peaks])
        # Compute frequency on the mean of all time points corresponding to the peak
        freq = 1 / np.mean(t_intervals)
        # Compute amplitude
        amplitude = np.max(population) - np.min(population)

        return amplitude, freq
    
    predator_pop = sol[:, 1]
    prey_pop = sol[:, 0]

    predator_amplitude, predator_freq = Ampl_Freq_population(t, predator_pop)
    prey_amplitude, prey_freq = Ampl_Freq_population(t, prey_pop)
    
    return prey_amplitude, prey_freq, predator_amplitude, predator_freq
