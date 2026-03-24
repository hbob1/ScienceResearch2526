import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# --- Coil and simulation parameters ---
mu0 = 4*np.pi*1e-7
I = 7
N = 600
R = 0.04
d = R
n_segments = 200
theta = np.linspace(0, 2*np.pi, n_segments)

# Coil coordinates
coil1_x = R * np.cos(theta)
coil1_y = R * np.sin(theta)
coil2_y = R * np.cos(theta)
coil2_z = R * np.sin(theta)

# --- Biot-Savart calculation ---
def B_field_point(x, y, z):
    B = np.zeros(3)
    # First pair along z-axis
    for z0 in [-d/2, d/2]:
        for i in range(n_segments-1):
            r1 = np.array([coil1_x[i], coil1_y[i], z0])
            r2 = np.array([coil1_x[i+1], coil1_y[i+1], z0])
            dl = r2 - r1
            r_vec = np.array([x, y, z]) - r1
            r_mag = np.linalg.norm(r_vec)
            if r_mag != 0:
                B += np.cross(dl, r_vec) / r_mag**3

    # Second pair along x-axis
    for x0 in [-d/2, d/2]:
        for i in range(n_segments-1):
            r1 = np.array([x0, coil2_y[i], coil2_z[i]])
            r2 = np.array([x0, coil2_y[i+1], coil2_z[i+1]])
            dl = r2 - r1
            r_vec = np.array([x, y, z]) - r1
            r_mag = np.linalg.norm(r_vec)
            if r_mag != 0:
                B += np.cross(dl, r_vec) / r_mag**3

    B *= mu0 * I * N / (4*np.pi)
    return B

# --- Grid for evaluation ---
grid_points = 20
grid = np.linspace(-0.06, 0.06, grid_points)
X, Y, Z = np.meshgrid(grid, grid, grid, indexing='ij')
Bmag = np.zeros_like(X)

# Compute B magnitude
for i in range(grid_points):
    for j in range(grid_points):
        for k in range(grid_points):
            Bmag[i,j,k] = np.linalg.norm(B_field_point(X[i,j,k], Y[i,j,k], Z[i,j,k]))

B0 = Bmag[grid_points//2, grid_points//2, grid_points//2]

# ±1% uniform region
uniform = np.abs(Bmag - B0)/B0 <= 0.01

# --- 3D mesh plot ---
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111, projection='3d')

# Extract surface of uniform region using marching cubes (or simple threshold)
from skimage import measure
verts, faces, normals, values = measure.marching_cubes(uniform, 0.5)
ax.plot_trisurf(verts[:, 0]*0.12/grid_points-0.06,  # scale back to physical units
                verts[:, 1]*0.12/grid_points-0.06,
                verts[:, 2]*0.12/grid_points-0.06,
                triangles=faces, color='green', alpha=0.6)
ax.set_xlabel('X [m]')
ax.set_ylabel('Y [m]')
ax.set_zlabel('Z [m]')
ax.set_title('3D ±1% Uniform Magnetic Field Volume')
plt.show()

# --- 2D slices for each plane ---
slices = {
    'X-Y plane (Z=0)': uniform[:,:,grid_points//2],
    'X-Z plane (Y=0)': uniform[:,grid_points//2,:],
    'Y-Z plane (X=0)': uniform[grid_points//2,:,:]
}

fig2, axs = plt.subplots(1,3, figsize=(15,4))
for ax, (title, data) in zip(axs, slices.items()):
    im = ax.imshow(data.T, origin='lower', extent=[-0.06,0.06,-0.06,0.06], cmap='Greens', alpha=0.6)
    ax.set_title(title)
    ax.set_xlabel('X [m]' if 'X' in title else 'Y [m]')
    ax.set_ylabel('Y [m]' if 'Y' in title else 'Z [m]')
    ax.set_aspect('equal')
fig2.suptitle('2D ±1% Uniform Magnetic Field Slices')
plt.show()
