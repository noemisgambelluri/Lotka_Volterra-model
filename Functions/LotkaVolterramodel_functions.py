#=======================================================================
# Author: Noemi Sgambelluri
# Date: 18 October, 2023
#
# Lotka-Volterra model (also known as 'Predator-Prey equations)
#
# Aim: To define the functions needed to simulate the Lotka-Volterra model.
#=======================================================================

def LotkaVolterra(variables, parameters):

    """

    This function defines the Lotka-Volterra equations for a two species system.

    Parameters
        variables : current population levels of the two interacting species
        parameters : parameters that define the interaction between the species

    Returns:
        Rates of change of both the prey and the predator populations (dxdt, dydt)

    """

    x, y = variables
    alpha, beta, delta, gamma = parameters

    #Mathematical implementation of the Lotka-Volterra equations:
    dxdt = alpha * x - beta * x * y
    dydt = delta * x * y - gamma * y

    return dxdt, dydt

def Equilibria(parameters):
        
    """
    This function computes the two equilibrium points, i.e. the population values at which both
    the predator and prey populations remain constant over time. 
    

    Parameters
        parameters : parameters that define the interaction between the species

    Returns:
        equilibrium points values
    """
    alpha, beta, delta, gamma = parameters

    #mathematical definition of the equilibrium points of the Lotka-Volterra equations
    eq_point1 = (0.0, 0.0)
    eq_point2 = (gamma/delta, alpha/beta)

    return eq_point1, eq_point2




    
    




