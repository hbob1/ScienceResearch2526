import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load CSV
df = pd.read_csv(r"C:\Users\marik\Documents\20251202\20251202_20260103_170614.csv")

# Convert timestamps to datetime
df['Timestamps'] = pd.to_datetime(df['Timestamps'])

# Normalize timestamps to hours since earliest timestamp
start_time = df['Timestamps'].min()
df['Hours'] = (df['Timestamps'] - start_time).dt.total_seconds() / 3600

# Get unique row/col pairs
row_col_pairs = sorted(df[['Row', 'Col']].drop_duplicates().values.tolist())

# X-axis positions
x = np.arange(len(row_col_pairs))
width = 0.35

# Data containers
camera1_heights = []
camera2_heights = []
camera1_labels = []
camera2_labels = []

for r, c in row_col_pairs:
    cam1 = df[(df['Row'] == r) & (df['Col'] == c) & (df['Grid'] == 'camera1')]
    cam2 = df[(df['Row'] == r) & (df['Col'] == c) & (df['Grid'] == 'camera2')]

    if not cam1.empty:
        camera1_heights.append(cam1['Hours'].iloc[0])
        camera1_labels.append(cam1['Timestamps'].iloc[0].strftime("%m-%d %H:%M"))
    else:
        camera1_heights.append(0)
        camera1_labels.append("")

    if not cam2.empty:
        camera2_heights.append(cam2['Hours'].iloc[0])
        camera2_labels.append(cam2['Timestamps'].iloc[0].strftime("%m-%d %H:%M"))
    else:
        camera2_heights.append(0)
        camera2_labels.append("")

# Plot
fig, ax = plt.subplots(figsize=(14, 6))

bars1 = ax.bar(x - width/2, camera1_heights, width, label='Camera 1')
bars2 = ax.bar(x + width/2, camera2_heights, width, label='Camera 2')

# Add timestamp labels above bars
for bar, label in zip(bars1, camera1_labels):
    if label:
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            label,
            ha='center', va='bottom', fontsize=8, rotation=90
        )

for bar, label in zip(bars2, camera2_labels):
    if label:
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            label,
            ha='center', va='bottom', fontsize=8, rotation=90
        )

# Formatting
ax.set_ylabel("Hours since first germination")
ax.set_xlabel("Row, Col")
ax.set_title("Germination Time by Grid Position (Timestamp Shown)")
ax.set_xticks(x)
ax.set_xticklabels([f"R{r}C{c}" for r, c in row_col_pairs])
ax.legend()

plt.tight_layout()
plt.show()
