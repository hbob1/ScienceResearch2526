import math

u = 1.25663706 * 10e-6
N = 200
I = 3
r = 0.07

L = r * 2

B = (u * N * I) / L

print(B*10000)