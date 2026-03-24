import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import marching_cubes

mu0 = 4*np.pi*1e-7
I = 3.0
N = 200
R = 0.07  # 10 cm radius
d = R      # Helmholtz separation

# Coil discretization
n_segments = 200
theta = np.linspace(0, 2*np.pi, n_segments)
coil_x = R * np.cos(theta)
coil_y = R * np.sin(theta)

def B_field_at_point(x, y, z):
    """Compute B field vector from two Helmholtz coils at point (x,y,z)."""
    B = np.zeros(3)
    for z0 in [-d/2, d/2]:
        for i in range(n_segments-1):
            r1 = np.array([coil_x[i], coil_y[i], z0])
            r2 = np.array([coil_x[i+1], coil_y[i+1], z0])
            dl = r2 - r1
            r_vec = np.array([x, y, z]) - r1
            r_mag = np.linalg.norm(r_vec)
            if r_mag != 0:
                B += np.cross(dl, r_vec) / (r_mag**3)
    B *= mu0 * I * N / (4*np.pi)
    return B

# Grid
n_grid = 25
grid = np.linspace(-0.05, 0.05, n_grid)  # ±5 cm
Bmag = np.zeros((n_grid, n_grid, n_grid))

for i, x in enumerate(grid):
    for j, y in enumerate(grid):
        for k, z in enumerate(grid):
            Bmag[i,j,k] = np.linalg.norm(B_field_at_point(x,y,z))

B0 = np.linalg.norm(B_field_at_point(0,0,0))

# Fractional deviation
frac_dev = np.abs(Bmag - B0)/B0

# Extract ±1% surface using marching cubes
verts, faces, _, _ = marching_cubes(frac_dev, level=0.01)

# Convert verts to cm
verts = verts / (n_grid-1) * (grid[-1]-grid[0]) + grid[0]
verts *= 100  # cm

# Plot mesh
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111, projection='3d')

mesh = Poly3DCollection(verts[faces], alpha=0.9)
mesh.set_facecolor("green")
ax.add_collection3d(mesh)

ax.set_xlim(-5,5)
ax.set_ylim(-5,5)
ax.set_zlim(-5,5)
ax.set_xlabel("X [cm]")
ax.set_ylabel("Y [cm]")
ax.set_zlabel("Z [cm]")
ax.set_title("3D Uniform Magnetic Field Region (±1%)")
plt.show()
