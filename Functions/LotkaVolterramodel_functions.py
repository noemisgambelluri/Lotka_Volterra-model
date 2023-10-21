

def LotkaVolterra(variables, parameters):
    # Define the Lotka-Volterra equations for a two specoes system
    # 'variables': array of the current population levels of the two interacting species
    # 't': represents time
    # 'parameters': array of parameters that define the interaction between the species

    x, y = variables
    alpha, beta, delta, gamma = parameters

    #Lotka-Volterra (also known as 'Predator-Prey) equations mathematical implementation:
    dxdt = alpha * x - beta * x * y
    dydt = delta * x * y - gamma * y

    #return the rates of change of both the prey and predator populations
    return dxdt, dydt


