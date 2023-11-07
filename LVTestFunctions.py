########################################################################
# Author: Noemi Sgambelluri
# Date: 28 October, 2023
#
# Tests of model functions
#
# Aim: To test functions in LotkaVolterraModel.py.
########################################################################

import numpy as np 
import hypothesis
from hypothesis import strategies as st
from hypothesis import given, settings
import LotkaVolterraModel as LVM 

def test_LotkaVolterra_computation():

    """
    Procedure:
    1. Initialize a random combination of parameters values
    2. Initialize variables (preys, predators) values
    3. Initialize time value
    3. Compute dxdt and dydt values to perform a validation test
    ---------
    Verification:
    3. The computation of dxdt performed by the function has to correspond to the expected
       computed dxdt value
    4. The computation of dydt performed by the function has to correspond to the expected
       computed dydt value
    """

    alpha = 1.2 
    beta = 0.5
    delta = 0.3
    gamma = 0.5
    variables = [15, 20]
    time  = 25
    dxdt, dydt = LVM.LotkaVolterra(variables, time, alpha, beta, delta, gamma)
    
    assert dxdt == -132.0
    assert dydt == 80.0
    
#possiamo testare che la funzione dia un errore per parametri negativi

@given(t_max = st.floats(1,50), num_points=st.integers(10,500))
def test_SolveLotkaVolterra_extinction(t_max, num_points):
    
   """
   Procedure:
   1. Configurate time interval for Lotka Volterra model given a maximum time  
   (t_max) and number of time points (num_points)
   2. Initialize preys and predators initial conditions as well as paramaters values
   that should lead to extinction of preys and predators
   3. Solve Lotka Volterra equations for each time point
   ---------
   Verification:
   4. Ensure the initial conditions match the first points in the solution
   5. Ensure that the final prey and predators' populations reach zero or close to zero (extinction)
   6. If this does not appen, raise an assertion error
   """

   alpha = 1.0
   beta = 1.0
   delta = 2.0
   gamma = 2.0
   initial_conditions = [1.0, 1.0]
   parameters = (alpha, beta, delta, gamma)
   
   solution, time = LVM.SolveLotkaVolterra(parameters, initial_conditions, t_max, num_points)
   
   # Check initial conditions match first points in solution
   assert solution[0, 0] == initial_conditions[0]
   assert solution[0, 1] == initial_conditions[1]

   final_prey_population = solution[-1, 0]
   final_pred_population = solution[-1, 1]

   # Check if the prey and predator population are not equal to 0 (extinction)
   assert final_prey_population == 0.0
   assert final_pred_population == 0.0

   
   #possiamo testare che se i predatori = 0, i prey crescono esponenzialmente
   #possiamo testare che se i prey = 0, i predator decrescono esponenzialmente


@given(t_max = st.floats(1,50), num_points=st.integers(10,500))
def test_SolveLotkaVolterra_length(t_max, num_points):

    """
    Procedure:
    1. Initialize random seed
    2. Configurate time interval for Lotka Volterra model given a maximum time  
    (t_max) and number of time points (num_points)
    3. Initialize preys and predators initial conditions and paramaters values
    4. Solve Lotka Volterra equations for each time point

    ---------
    Verification:
    3. The lenght of the solution array has to be the equal to the number of time points
    4. The solution has to be a 2D array 
    5. The lenght of the time array returned by the function has to be equal to the number 
       of time points
    6. All time points in the time array returned by the function has to be between 0 and 
       the max set time value
    """

    np.random.seed(5)
    initial_conditions = np.random.randint(2, high = 25, size = 2)
    parameters = np.random.uniform(0.1, high = 2.0, size = 4)
  
    solution, time = LVM.SolveLotkaVolterra(parameters, initial_conditions, t_max, num_points)

    assert len(solution) == num_points
    assert all(len(point) == 2 for point in solution) 
    assert len(time) == num_points
    assert all(0 <= t <= t_max for t in time)


@given(alpha = st.floats(0, 2.0), beta = st.floats(0.1, 2.0), delta = st.floats(0.1, 2.0), gamma = st.floats(0, 2.0))
def test_Equilibria_length(alpha, beta, delta, gamma):

    """
    Procedure:
    1. Initialize random seed
    2. Configurate the values for Lotka-volterra model parameters
    3. Compute equilibrium points

    ---------
    Verification:
    5. The lenght of the equilibrium points array has to be the equal to two
    6. The extinction equilibrium points has to have two coordinates
    7. The coexistence equilibrium points has to have two coordinates
    
    """

    np.random.seed(5)

    parameters = (alpha, beta, delta, gamma)
    eq_points = LVM.Equilibria(parameters)

    assert len(eq_points) == 2
    assert len(eq_points[0]) == 2
    assert len(eq_points[1]) == 2
   #possiamo testare che la forma matematica dei punti di equilibrio sia quella calcolando lo jacobiano: se i punti sono calcolati
   #correttamente allora la forma dello jacobiano deve essere quella

def test_Equilibria_computation():

    """
    Procedure:
    1. Initialize parameters values
    2. Manually compute equilibrium points values 
    ---------
    Verification:
    3. The extinction equilibrium point's coordinates values has to the computed values
    4. The coexistence equilibrium point's coordinates values has to the computed values
    """

    alpha = 1.0
    beta = 0.5
    delta = 0.2
    gamma = 0.5
    parameters = (alpha, beta, delta, gamma)
    eq_points = LVM.Equilibria(parameters)

    assert eq_points[0] == (0.0, 0.0)
    assert eq_points[1] == (2.5, 2.0) 
