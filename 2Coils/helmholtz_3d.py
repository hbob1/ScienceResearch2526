import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Constants
u0 = 4 * np.pi * 1e-7  # N/A^2
R = 0.065

# Sweep I and R
I_vals = np.linspace(0, 10, 100)         # Current in Amps
n_vals = np.linspace(50, 300, 100)   #50 turns to 1000 turns

# Create 2D grid for I and R
I, n = np.meshgrid(I_vals, n_vals)

# Calculate B field (using fixed n)
B = pow((4/5), 1.5) * (u0 * n * I) / R
BGauss = B * 10000
# Plotting
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

surf = ax.plot_surface(I, n, BGauss, cmap='viridis')
fig.colorbar(surf, label='Magnetic Field B (Gauss)')

ax.set_xlabel('Current I (Amps)')
ax.set_ylabel('Number of Turns')
ax.set_zlabel('Magnetic Field B (Gauss)')
ax.set_title('Magnetic Field B vs Current and Radius (Radius: ' + str(R) + ')')

plt.show()
