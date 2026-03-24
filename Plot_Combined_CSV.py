import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

csv_path = r"C:\Users\marik\Documents\000\2025\ScienceResearch_2025_26\Data\Combined_CSV\group_1_combined.csv"
filename = os.path.basename(csv_path)
name_no_ext = os.path.splitext(filename)[0]
df = pd.read_csv(csv_path)

df['Timestamps'] = pd.to_datetime(df['Timestamps'])

df['StartTime'] = pd.to_datetime(df['SourceFile'].str.replace('.csv', ''), format='%Y%m%d_%H%M%S')
df['Hours'] = (df['Timestamps'] - df['StartTime']).dt.total_seconds() / 3600

camera1_hours = df[df['Grid'] == 'camera1']['Hours'].values
camera2_hours = df[df['Grid'] == 'camera2']['Hours'].values

nmf = camera1_hours[camera1_hours > 0]
mf = camera2_hours[camera2_hours > 0]

mf_mean = np.mean(mf)
mf_median = np.median(mf)
mf_std = np.std(mf, ddof=1)

nmf_mean = np.mean(nmf)
nmf_median = np.median(nmf)
nmf_std = np.std(nmf, ddof=1)

rng = np.random.default_rng(42)
x_nmf = np.zeros(len(nmf)) + rng.normal(0, 0.04, size=len(nmf))   # LEFT
x_mf = np.ones(len(mf)) + rng.normal(0, 0.04, size=len(mf))     # RIGHT


plt.figure(figsize=(7, 6))

# Scatter points
plt.scatter(x_mf, mf, alpha=0.7, s=60, label="MF", color='tab:orange')
plt.scatter(x_nmf, nmf, alpha=0.7, s=60, label="No MF", color='tab:blue')

plt.hlines(nmf_mean, -0.25, 0.25, linewidth=3, color='tab:blue', linestyle='-', label=f'Mean: {nmf_mean:.2f}h')
plt.hlines(mf_mean, 0.75, 1.25, linewidth=3, color='tab:orange', linestyle='-', label=f'Mean: {mf_mean:.2f}h')

plt.hlines(nmf_median, -0.25, 0.25, linewidth=2, color='tab:blue', linestyle='--', alpha=0.7, label=f'Median: {nmf_median:.2f}h')
plt.hlines(mf_median, 0.75, 1.25, linewidth=2, color='tab:orange', linestyle='--', alpha=0.7, label=f'Median: {mf_median:.2f}h')
plt.fill_between(
    [-0.25, 0.25],
    nmf_mean - nmf_std,
    nmf_mean + nmf_std,
    alpha=0.2,
    color='tab:blue'
)

plt.fill_between(
    [0.75, 1.25],
    mf_mean - mf_std,
    mf_mean + mf_std,
    alpha=0.2,
    color='tab:orange'
)

# =========================
# Formatting
# =========================

plt.xticks([0, 1], ["No MF", "MF"])
plt.ylabel("Time to Germination (hours)")
plt.title("Seed Germination Time 3A")

plt.grid(axis="y", linestyle="--", alpha=0.4)
plt.xlim(-0.5, 1.5)


plt.legend(loc='upper right', fontsize=9)
plt.tight_layout()
plt.show()

# Print statistics
print(f"MF (Magnetic Field):")
print(f"  Mean: {mf_mean:.2f} hours")
print(f"  Median: {mf_median:.2f} hours")
print(f"  Std Dev: {mf_std:.2f} hours")
print(f"  Count: {len(mf)}")
print(f"\nNo MF (Control):")
print(f"  Mean: {nmf_mean:.2f} hours")
print(f"  Median: {nmf_median:.2f} hours")
print(f"  Std Dev: {nmf_std:.2f} hours")
print(f"  Count: {len(nmf)}")