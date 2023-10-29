########################################################################
# Author: Noemi Sgambelluri
# Date: 28 October, 2023
#
# Tests
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
    1. Initialize random seed
    2. Generate initial configuration given a certain number of particles (num_part) and linear dimension of space (space_dim)
    ---------
    Verification:
    3. The lenght of the output is 3
    4. The lenght of the output components (coordinates x, y and orietations of the particles) is num_part
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

@given(t_max = st.floats(1,50), num_points=st.integers(10,500))
def test_SolveLotkaVolterra_length(t_max, num_points):

    """
    Procedure:
    1. Initialize random seed
    2. Generate initial configuration given a certain number of particles (num_part) and linear dimension of space (space_dim)
    ---------
    Verification:
    3. The lenght of the output is 3
   4. The lenght of the output components (coordinates x, y and orietations of the particles) is num_part
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

    np.random.seed(5)

    parameters = (alpha, beta, delta, gamma)
    eq_points = LVM.Equilibria(parameters)

    assert len(eq_points) == 2
    assert len(eq_points[0]) == 2
    assert len(eq_points[1]) == 2


def test_Equilibria_computation():

    """
    Procedure:
    1. Initialize random seed
    2. Generate initial configuration given a certain number of particles (num_part) and linear dimension of space (space_dim)
    ---------
    Verification:
    3. The lenght of the output is 3
    4. The lenght of the output components (coordinates x, y and orietations of the particles) is num_part
    """

    alpha = 1.0
    beta = 0.5
    delta = 0.2
    gamma = 0.5
    parameters = (alpha, beta, delta, gamma)
    eq_points = LVM.Equilibria(parameters)

    assert eq_points[0] == (0.0, 0.0)
    assert eq_points[1] == (2.5, 2.0) 





test_LotkaVolterra_computation()
test_SolveLotkaVolterra_length()    
test_Equilibria_length()
test_Equilibria_computation()