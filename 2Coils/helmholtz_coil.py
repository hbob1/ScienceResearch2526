import numpy as np
import matplotlib.pyplot as plt

R = 0.07
u0 = 4 * np.pi * pow(10, -7) # newtons per amp squared
I_vals = np.linspace(0, 5, 100)
n_vals = np.linspace(50, 300, 100)

I, n = np.meshgrid(I_vals, n_vals)

B = pow((4/5), (3/2)) * (u0 * n * I) / R
BGauss = 10000 * B

plt.figure(figsize=(10, 6))
cp = plt.contourf(I, n, BGauss, levels=50, cmap='viridis')
plt.colorbar(cp, label='Magnetic Field B (Gauss)')
plt.xlabel('Current I (Amps)')
plt.ylabel('Number of Turns n')
plt.title('Magnetic Field B vs Current and Number of Turns')
plt.grid(True)
plt.show()

