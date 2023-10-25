# Lotka-Volterra model

The Lotka-Volterra model, names after Alfred Lotka and Vito Volterra, is a set of differential equations used to describe the dynamics of biological systems, particularly in the context of predator-prey relationships. It's a fundamental tool in ecology and population biology for understanding how the populations of species interact with each other over time. 

The aim of this project is to simulate the Lotka-Volterra model for *two species*. The goal is to offers a quantitative understanding of the dynamics within a simplified predator-prey ecosystem and to convey these dynamics visually through animations. These animations will depict the fluctuations in both predator and prey populations over time and demonstrate their interdependence in phase space.

To clone the repository and initiate the simulation, the user should utilize the specified command line syntax, subsequently enabling the visualization of the animation:

    gitclone https://github.com/noemisgambelluri/Lotka_Volterra-model.git
    cd Lotka_Volterra-model

    python Simulation.py settings.ini
    python Animation.py settings.ini

## Introduction to the model

The lotka-volterra equations are a pair of first-order nonlinear differential equations used to  describe predator-prey interaction, in particular how one population is affected by the other and vicevrsa. the population change through time according to the pair of equations:

$$\frac{dx}{dt} = \alpha x - \beta xy$$
$$\frac{dy}{dt} = \delta x y - \gamma y$$

where 
* the variable *x* is the population density of **prey** (for example, the number of fishes per square kilometre);
* the variable *y* is the population density of some **predator** (for example, the number of bears per square kilometre);
* $\frac{dy}{dt}$ and $\frac{dx}{dt}$ represent the instantaneous growth rates of the two populations;
* *t* represents time;
* The prey's parameters, $\alpha$ and $\beta$, describe, respectively, the maximum prey per capita growth rate, and the effect of the presence of predators on the prey growth rate.
* The predator's parameters, $\gamma$, $\delta$, respectively describe the predator's per capita death rate, and the effect of the presence of prey on the predator's growth rate.
All parameters are positive and real.

The solution of the differential equations is deterministic and continuous. This, in turn, implies that the generations of both the predator and prey are continually overlapping.

### Model Assumptions
