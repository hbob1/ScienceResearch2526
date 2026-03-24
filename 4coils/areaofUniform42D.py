import numpy as np
import matplotlib.pyplot as plt

# --- Coil and simulation parameters ---
mu0 = 4 * np.pi * 1e-7
I = 7
N = 500
R = 0.04  # 4 cm radius
d = R  # separation
n_segments = 200 # fewer segments for speed
theta = np.linspace(0, 2 * np.pi, n_segments)

# Coil coordinates
coil1_x = R * np.cos(theta)
coil1_y = R * np.sin(theta)
coil2_y = R * np.cos(theta)
coil2_z = R * np.sin(theta)


# --- Biot-Savart calculation ---
def B_field_point(x, y, z):
    B = np.zeros(3)
    # First pair along z-axis
    for z0 in [-d / 2, d / 2]:
        for i in range(n_segments - 1):
            r1 = np.array([coil1_x[i], coil1_y[i], z0])
            r2 = np.array([coil1_x[i + 1], coil1_y[i + 1], z0])
            dl = r2 - r1
            r_vec = np.array([x, y, z]) - r1
            r_mag = np.linalg.norm(r_vec)
            if r_mag != 0:
                B += np.cross(dl, r_vec) / r_mag ** 3

    # Second pair along x-axis (perpendicular)
    for x0 in [-d / 2, d / 2]:
        for i in range(n_segments - 1):
            r1 = np.array([x0, coil2_y[i], coil2_z[i]])
            r2 = np.array([x0, coil2_y[i + 1], coil2_z[i + 1]])
            dl = r2 - r1
            r_vec = np.array([x, y, z]) - r1
            r_mag = np.linalg.norm(r_vec)
            if r_mag != 0:
                B += np.cross(dl, r_vec) / r_mag ** 3

    B *= mu0 * I * N / (4 * np.pi)
    return B


# --- Grid parameters for fast 2D slices ---
grid_points = 60  # decent resolution
grid = np.linspace(-0.06, 0.06, grid_points)


def compute_slice(plane='XY', fixed=0.0):
    Bmag = np.zeros((grid_points, grid_points))

    for i, xi in enumerate(grid):
        for j, yj in enumerate(grid):
            if plane == 'XY':
                B = B_field_point(xi, yj, fixed)
            elif plane == 'XZ':
                B = B_field_point(xi, fixed, yj)
            elif plane == 'YZ':
                B = B_field_point(fixed, xi, yj)
            Bmag[i, j] = np.linalg.norm(B)

    B0 = Bmag[grid_points // 2, grid_points // 2]
    uniform = np.abs(Bmag - B0) / B0 <= 0.01
    return uniform, Bmag, B0


# --- Plotting 2D slices ---
planes = ['XY', 'XZ', 'YZ']
fig, axs = plt.subplots(1, 3, figsize=(18, 5))

for ax, plane in zip(axs, planes):
    uniform, Bmag, B0 = compute_slice(plane=plane, fixed=0.0)
    ax.contourf(grid * 100, grid * 100, uniform.T, levels=1, cmap='Greens', alpha=0.6)
    ax.contour(grid * 100, grid * 100, (Bmag - B0) / B0 * 100, levels=[-1, 1], colors='red')
    ax.set_xlabel(plane[0] + ' [cm]')
    ax.set_ylabel(plane[1] + ' [cm]')
    ax.set_title(f'{plane} plane ±1% uniform region')
    ax.set_aspect('equal')

plt.suptitle('2D ±1% Uniform Magnetic Field Slices (4 Perpendicular Coils)')
plt.show()
