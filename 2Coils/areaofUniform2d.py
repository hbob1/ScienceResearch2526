import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

mu0 = 4*np.pi*1e-7
I = 3
N = 200
R = 0.065  # 10 cm radius
d = R     # Helmholtz separation

# Coil discretization (for Biot–Savart)
n_segments = 200
theta = np.linspace(0, 2*np.pi, n_segments)
coil_x = R * np.cos(theta)
coil_y = R * np.sin(theta)

def B_field_at_point(x, y, z):
    """Compute B field vector from two Helmholtz coils at point (x,y,z)."""
    B = np.zeros(3)
    # Two coils: one at +d/2, one at -d/2 along z
    for z0 in [-d/2, d/2]:
        for i in range(n_segments-1):
            # Segment endpoints
            r1 = np.array([coil_x[i], coil_y[i], z0])
            r2 = np.array([coil_x[i+1], coil_y[i+1], z0])
            dl = r2 - r1
            r_vec = np.array([x, y, z]) - r1
            r_mag = np.linalg.norm(r_vec)
            if r_mag != 0:
                B += np.cross(dl, r_vec) / (r_mag**3)
    B *= mu0 * I * N / (4*np.pi)
    return B

# Grid for evaluation (cross-section in x-z plane at y=0)
grid = np.linspace(-0.1, 0.1, 50)  # -10cm to +10cm
X, Z = np.meshgrid(grid, grid)
Bx, Bz = np.zeros_like(X), np.zeros_like(Z)

for i in range(len(grid)):
    for j in range(len(grid)):
        B = B_field_at_point(X[i,j], 0, Z[i,j])
        Bx[i,j], Bz[i,j] = B[0], B[2]

Bmag = np.sqrt(Bx**2 + Bz**2)
B0 = Bmag[len(grid)//2, len(grid)//2]

# Mask uniform region (±1%)
uniform = np.abs(Bmag - B0) / B0 <= 0.1

plt.figure(figsize=(6,6))
orange_map = LinearSegmentedColormap.from_list(
    "high_contrast_orange",
    ["#fff1dc", "#cc4a00"]  # very light → very dark orange
)

plt.contourf(X*100, Z*100, uniform, levels=1, cmap=orange_map, alpha=0.7)


#plt.contour(X*100, Z*100, (Bmag-B0)/B0*100, levels=[-1,1], colors="red")
plt.xlabel("X [cm]")
plt.ylabel("Z [cm]")
plt.title("Uniform Magnetic Field Region (±10%) in X-Z plane")
plt.gca().set_aspect("equal")
plt.show()
