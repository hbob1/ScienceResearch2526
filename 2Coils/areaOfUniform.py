import numpy as np
import matplotlib.pyplot as plt
mu0 = 4*np.pi*1e-7
I = 3
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

# Grid of points
grid = np.linspace(-0.05, 0.05, 15)  # ±5 cm region
points = []
Bcenter = np.linalg.norm(B_field_at_point(0,0,0))

for x in grid:
    for y in grid:
        for z in grid:
            B = B_field_at_point(x,y,z)
            Bmag = np.linalg.norm(B)
            if np.abs(Bmag - Bcenter)/Bcenter <= 0.01:  # ±1%
                points.append([x,y,z])

points = np.array(points)

# Plot 3D region
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(points[:,0]*100, points[:,1]*100, points[:,2]*100,
           c='green', s=10, alpha=0.6, label="±1% uniform region")
ax.set_xlabel("X [cm]")
ax.set_ylabel("Y [cm]")
ax.set_zlabel("Z [cm]")
ax.set_title("3D Uniform Magnetic Field Region (±1%)")
ax.legend()
plt.show()
