import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

u0 = 4 * np.pi * 1e-7
I = 3
n = 200
R = 0.065


x = np.linspace(-0.1, 0.1, 20)
z = np.linspace(-0.1, 0.1, 20)
X, Z = np.meshgrid(x, z)
Y = np.zeros_like(X)

r = np.sqrt(X**2 + Y**2)

def Bz_coil(r, z, z0):
    return (u0 * n * I * R**2) / (2 * ((R**2 + (z - z0)**2 + r**2)**1.5))

z1 = -R / 2
z2 = R / 2

Bz_total = Bz_coil(r, Z, z1) + Bz_coil(r, Z, z2)
Bz_totalGauss = Bz_total * 10000

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

from matplotlib.colors import LinearSegmentedColormap

blue_orange = LinearSegmentedColormap.from_list(
    "blue_orange",
    ["#1f77b4", "#ff7f0e"]
)

surf = ax.plot_surface(X, Z, Bz_totalGauss, cmap=blue_orange, linewidth=0, antialiased=False)


ax.set_title('Magnetic Field (B) in x-z')
ax.set_xlabel('x (meters)')
ax.set_ylabel('z (meters)')
ax.set_zlabel('Magnetic Field B (Gauss')

fig.colorbar(surf, shrink=0.5, aspect=10, label='B (Gauss)')
plt.tight_layout()
plt.show()
