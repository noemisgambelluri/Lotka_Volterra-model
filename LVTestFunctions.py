########################################################################
# Author: Noemi Sgambelluri
# Date: 28 October, 2023
#
# Tests of model functions
#
# Aim: To test functions in LotkaVolterraModel.py.
########################################################################

import numpy as np 
from scipy.linalg import eigvals
from scipy.signal import find_peaks
from sympy import symbols, Eq, solve
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
   4. Compute dxdt and dydt values to perform a validation test
    ---------
   Verification:
   5. The computation of dxdt performed by the function has to correspond to the expected
       computed dxdt value
   6. The computation of dydt performed by the function has to correspond to the expected
       computed dydt value
   7. Check the computation with negative parameters raises error 
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

   # Check Lotka-Volterra model with negative parameters
   negative_alpha = -1.2
   try:
      dxdt, dydt = LVM.LotkaVolterra(variables, time, negative_alpha, beta, delta, gamma)
      # If there's no error, raise an AssertionError to indicate the test failure
      raise AssertionError("Expected an error with negative parameters, but no error was raised.")

   except Exception as e:
        # Check that the exception message contains a specific error message related to negative parameters
        assert "Negative parameters are not allowed" in str(e)
    

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
   5. Ensure that the final prey and predators' populations reach zero or close 
   to zero (extinction)
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

   # Check if the prey and predator population are equal to 0 (extinction)
   assert final_prey_population == 0.0
   assert final_pred_population == 0.0


@given(alpha = st.floats(0, 2.0), beta = st.floats(0.1, 2.0), delta = st.floats(0.1, 2.0), gamma = st.floats(0, 2.0), t_max = st.floats(1,50), num_points=st.integers(10,500))
def test_SolveLVBothScenarios(alpha, beta, delta, gamma, t_max, num_points):

   """
   Procedure:
   1. Configurate time interval for Lotka Volterra model given a maximum time  
   (t_max) and number of time points (num_points)
   2. Configurate the model parameters values
   3. Initialize preys and predators initial conditions scenarios 
   that should lead to exponential decrease of predators and 
   exponential growth of preys
   4. For loop changing the scenarios and solve Lotka Volterra equations 
   for each time point of each scenario
   ---------
   Verification:
   5. Check if the preys population remains zero 
   6. Check if the predators populations exhibits exponential decrease
   7. Check if the predators population remains zero
   8. Check if the preys population exhibits exponential growth
   """

   parameters = (alpha, beta, delta, gamma)
   scenarios = [("Initial prey population as zero", [0.0, 10.0]), ("Initial predator population as zero", [10.0, 0.0])]

   for scenario_name, initial_conditions in scenarios:
      # Call the SolveLotkaVolterra function for the current scenario
      solution, time = LVM.SolveLotkaVolterra(parameters, initial_conditions, t_max, num_points)
   
      # Check if the corresponding population remains zero
      final_prey_population = solution[-1, 0]
      final_pred_population = solution[-1, 1]

      if "prey" in scenario_name:
         # Check if the prey population is zero
         assert final_prey_population == 0.0

         # Check if the predators population exhibits exponential decrease
         initial_pred_pop = initial_conditions[1]
         expected_decrease = initial_pred_pop / (np.exp(gamma * t_max))
         assert final_pred_population == expected_decrease

      else:
         # Check if the predator population remains zero
         assert final_pred_population == 0.0

         # Check if the prey population exhibits exponential growth
         initial_prey_pop = initial_conditions[0]
         expected_growth = initial_prey_pop * np.exp(alpha * t_max)
         assert final_prey_population == expected_growth

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


def test_EquilibriumPoints():

   """
   Procedure:
    1. Initialize Lotka-Volterra parameters as symbols
    2. Define mathematically the Lotka-Volterra equations
    3. Solve the equations for x and y to find equilibrium points
    4. Give a set of values to Lotka-Volterra parameters
    5. Call the Equilibria function to compute equilibrium points for those values

    ---------
    Verification: 
    6. The extinction equilibrium points has to have two coordinates
    
   """
   # Define the Lotka-Volterra parameters
   alpha, beta, delta, gamma = symbols('alpha beta delta gamma')
   x, y = symbols('x y')

   # Define the Lotka-Volterra equations
   equations = [Eq(alpha * x - beta * x * y, 0), Eq(delta * x * y - gamma * y, 0)]

   # Solve the equations for x and y
   equilibrium_points_formula = solve(equations, (x, y))

   # Test the critical points against the Equilibria function
   parameters = [1.0, 2.0, 3.0, 4.0]
   eq_point1, eq_point2 = LVM.Equilibria(parameters)

   # Check if both sets of critical points are close
   assert [point[0].evalf() for point in equilibrium_points_formula] == eq_point1
   assert [point[1].evalf() for point in equilibrium_points_formula] == eq_point2


def LotkaVolterraJacobian(x, *parameters):
    
    """
    Jacobian matrix for the Lotka-Volterra equations.
    """

    alpha, beta, delta, gamma = parameters

    J = np.array([
        [alpha - beta * x[1], -beta * x[0]],
        [delta * x[1], delta * x[0] - gamma]
    ])

    return J

def test_Equilibria():
   
   """
   Procedure:
   1. Define a function that check stability of an equilibirum point using known jacobian eigenvalues
   2. Give all zero parameters
   3. Give non-zero parameters

   ---------
   Verification:
   5. Equilibirum points are zero and infinite with all zero parameters, check point is stable otherwise raise error
   6. Equilibrium points have expected computed values with non-zero parameters, 
   chech points are stable otherwise raise error
   """

   def check_stability(eq_point, parameters):
      """
      Check the stability of an equilibrium point using Jacobian eigenvalues.
      """
      J = LotkaVolterraJacobian(eq_point, *parameters)
      eigenvalues = eigvals(J)
      # If all eigenvalues have negative real parts, the equilibrium point is stable
      assert all(np.real(eigenvalues) < 0), f"Unstable equilibrium point: {eq_point}"

   # Test case 1: Equilibrium points with zero parameters
   parameters_zero = [0.0, 0.0, 0.0, 0.0]
   eq_point1, eq_point2 = LVM.Equilibria(parameters_zero)
   assert eq_point1 == [0.0, 0.0]
   assert eq_point2 == [float('inf'), float('inf')]  # Expecting infinity for division by zero

   # Check stability of equilibrium points
   check_stability(eq_point1, parameters_zero)
   # Note: Stability of eq_point2 is not checked here due to division by zero

   # Test case 2: Equilibrium points with non-zero parameters
   parameters_nonzero = [2.0, 1.0, 2.5, 4.0]
   eq_point1, eq_point2 = LVM.Equilibria(parameters_nonzero)
   assert eq_point1 == [0.0, 0.0]
   assert eq_point2 == [1.6, 0.5]

   # Check stability of equilibrium points
   check_stability(eq_point1, parameters_nonzero)
   check_stability(eq_point2, parameters_nonzero)


def test_AmplitudeFrequency():

   """
   Procedure:
   1. Define a mock time interval  
   2. Define prey and predators population oscillation patterns as sinusoidals
   3. Call the Amplitude and Frequency function to compute amplitude and frequencies

   ---------
   Verification:
   4. If the computation performed by the function is correct, prey and predators amplitude and
   frequencies must match expected values
   """

   # Mock data for testing
   t = np.linspace(0, 10, 100)
   prey_population = np.sin(2 * np.pi * 0.5 * t)  # Example sinusoidal prey population
   predator_population = np.cos(2 * np.pi * 0.5 * t)  # Example sinusoidal predator population
   sol = np.column_stack((prey_population, predator_population))

   # Call the function to calculate amplitude and frequency
   prey_amplitude, prey_freq, predator_amplitude, predator_freq = LVM.AmplitudeandFrequency(sol, t)

   # Perform assertions to check if the results match expectations
   assert prey_amplitude == 1.0
   assert prey_freq == 0.5
    
   assert predator_amplitude == 1.0
   assert predator_freq == 0.5

@given(t_max = st.floats(1,50), num_points=st.integers(10,500))
def test_AmplFreqValues(solution, time):

   """
   Procedure:
   1. Configurate time interval for Lotka Volterra model given a maximum time  
   (t_max) and number of time points (num_points)
   2. define Lotka-Volterra parameters
   3. Solve Lotka Volterra equations for each time point
   4. Compute amplitude and frequency for each population's oscillation pattern

   ---------
   Verification:
   5. The prey population oscillation pattern's frequency and amplitude must be smaller or equal to 1
   6. The predator population oscillation pattern's frequency and amplitude must be smaller or equal to 1
   """

   np.random.seed(5)

   alpha = 1.0
   beta = 1.0
   delta = 2.0
   gamma = 2.0
   initial_conditions = [1.0, 1.0]
   parameters = (alpha, beta, delta, gamma)
   
   # Solve the equations with the above parameters
   solution, time = LVM.SolveLotkaVolterra(parameters, initial_conditions, t_max, num_points)

   # Call the function to calculate amplitude and frequency
   prey_amplitude, prey_freq, predator_amplitude, predator_freq = LVM.AmplitudeandFrequency(solution, time)

   #check if frequencies and amplitude are smaller or equal to 1 as they should be
   assert prey_freq <= 1.0
   assert prey_amplitude <= 1.0
   assert predator_freq <= 1.0
   assert predator_amplitude <= 1.0