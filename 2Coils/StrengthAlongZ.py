import numpy as np
import matplotlib.pyplot as plt

u0 = 4 * np.pi * 1e-7
I = 3
n = 200
R = 0.07

z = np.linspace(-0.3, 0.3, 1000)

def B_coil(z, z0):
    return (u0 * n * I * R**2) / (2 * ((R**2 + (z - z0)**2)**(1.5)))

z1 = -R / 2
z2 = R / 2

B1 = B_coil(z, z1)
B1Gauss = B1 * 10000
B2 = B_coil(z, z2)
B2Gauss = B2 * 10000
B_total = B1 + B2
B_totalGauss = B_total * 10000

B_center = B_total[np.abs(z) < 0.001][0]
tolerance = 0.01
equalField = np.abs(B_total - B_center) <= B_center * tolerance
B_uniform = np.where(equalField, B_total, np.nan)
B_uniformGauss = B_uniform * 10000

plt.figure(figsize=(10, 6))
plt.plot(z, B1Gauss, label='Coil 1 Field', linestyle='--', color='red')
plt.plot(z, B2Gauss, label='Coil 2 Field', linestyle='--', color='blue')
plt.plot(z, B_totalGauss, label='Total Field', linewidth=2, color='purple')
plt.plot(z, B_uniformGauss, label='Uniform Field Region (+-1%)', linewidth=4, color='green')

plt.xlim(-0.075, 0.075 )

plt.title('Magnetic Field Along the Axis')
plt.xlabel('Position z (meters)')
plt.ylabel('Magnetic Field B (Gauss)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
