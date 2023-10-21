import numpy as np
import matplotlib.pyplot as plt

# Define the parameters
alpha = 0.1
beta = 0.02
delta = 0.3
gamma = 0.01

# Create a grid of x and y values
x = np.linspace(0.01, 5, 400)
y = np.linspace(0.01, 5, 400)
X, Y = np.meshgrid(x, y)

# Calculate the function V
V = delta * X - gamma * np.log(X) + beta * Y - alpha * np.log(Y)

# Create a 3D surface plot of V
fig = plt.figure(figsize=(10, 8))
ax = fig.gca(projection='3d')
ax.plot_surface(X, Y, V, cmap='viridis')

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('V')
ax.set_title('Surface Plot of V')

plt.show()