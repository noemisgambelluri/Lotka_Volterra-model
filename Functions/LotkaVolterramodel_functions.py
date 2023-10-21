#=======================================================================
# Author: Noemi Sgambelluri
# Date: 15 October, 2023
#
# Lotka-Volterra model (also known as 'Predator-Prey equations)
#
# Aim: To define the functions needed to simulate the Lotka-Volterra model.
#=======================================================================

import numpy as np
from scipy.integrate import find_peaks
from scipy.integrate import odeint
from scipy.signal import find_peaks

def LotkaVolterra(variables, parameters):

    """

    This function defines the Lotka-Volterra equations for a two species system.

    Parameters:
        variables : array
            A list containing current population levels of the two interacting species.

        parameters : float
            Lotka-Volterra model parameters that define the interaction between the species.

    Returns:
        Rates of change of both the prey and the predator populations (dxdt, dydt).

    """

    x, y = variables
    alpha, beta, delta, gamma = parameters

    #Mathematical implementation of the Lotka-Volterra equations:
    dxdt = alpha * x - beta * x * y
    dydt = delta * x * y - gamma * y

    return dxdt, dydt

def SolveLotkaVolterra(parameters, initial_conditions, t_max, num_points):
   
    """

    Numerically solve the Lotka-Volterra equations.

    Parameters:
    parameters : float
        Lotka-Volterra model parameters.

    initial_conditions : float
        Initial populations of prey and predator.

    t_max : float
        Maximum time for simulation.

    num_points : int
        Number of time points for simulation.

    Returns:
    solution : array
        An array containing the prey and predator populations at different time points.
    t : array
        An array containing the time points.

    """
    #create a time vector
    t = np.linspace(0, t_max, num_points)
    #set initial conditions
    x0, y0 = initial_conditions
    alpha, beta, delta, gamma = parameters
    #numerically solve the Lotka-Volterra equations
    sol = odeint(LotkaVolterra, initial_conditions, t, args= (alpha, beta, delta, gamma))

    return sol, t 

def Equilibria(parameters):
        
    """

    This function computes the two equilibrium points (steady-states solutions), i.e. the population 
    values at which both the predator and prey populations remain constant over time. 
     

    Parameters
        parameters : parameters (alpha, beta, delta, gamma) that define the interaction between the species

    Returns:
        two types of population equilibrium points: Extinction equilibrium point (eq_point1) 
        and Coexistence equilibrium point (eq_point2).

    """
    alpha, beta, delta, gamma = parameters

    #mathematical definition of the equilibrium points of the Lotka-Volterra equations
    eq_point1 = (0.0, 0.0)
    eq_point2 = (gamma/delta, alpha/beta)

    return eq_point1, eq_point2






    
    




