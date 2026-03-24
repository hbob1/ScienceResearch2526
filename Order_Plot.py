import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

csv_path = r"C:\Users\marik\Documents\000\2025\ScienceResearch_2025_26\Data\Combined_CSV\group_3_combined.csv"
output_path = r"C:\Users\marik\Documents\000\2025\ScienceResearch_2025_26\Data\Plots\GerminationTimeline"

# Create output directory if it doesn't exist
os.makedirs(output_path, exist_ok=True)

# Read the combined CSV
df = pd.read_csv(csv_path)

# Convert timestamps to datetime
df['Timestamps'] = pd.to_datetime(df['Timestamps'])
df['StartTime'] = pd.to_datetime(df['SourceFile'].str.replace('.csv', ''), format='%Y%m%d_%H%M%S')

# Calculate hours since experiment start for each row
df['Hours'] = (df['Timestamps'] - df['StartTime']).dt.total_seconds() / 3600

# Filter out non-positive values
df = df[df['Hours'] > 0].copy()

# Sort by germination time (Hours)
df = df.sort_values('Hours').reset_index(drop=True)

# Add germination order number
df['GermOrder'] = range(1, len(df) + 1)

# Assign colors based on Grid
df['Color'] = df['Grid'].map({'camera1': '#1f77b4', 'camera2': '#ff7f0e'})  # Blue for No MF, Orange for MF
df['Label'] = df['Grid'].map({'camera1': 'No MF', 'camera2': 'MF'})

# =========================
# Create Plot
# =========================

fig, ax = plt.subplots(figsize=(10, 12))

# Create horizontal bars for each seed
bar_height = 1.0
for idx, row in df.iterrows():
    ax.barh(row['GermOrder'], row['Hours'], height=bar_height,
            color=row['Color'], alpha=0.7, linewidth=0.5)

# Formatting
ax.set_xlabel('Time to Germination (hours)', fontsize=12)
ax.set_ylabel('Germination Order', fontsize=12)
ax.set_title('Seed Germination Timeline No Power', fontsize=14, fontweight='bold')

# Set y-axis to show all germination orders
ax.set_ylim(0.5, len(df) + 0.5)
ax.invert_yaxis()  # First germinated at top

# Grid
ax.grid(axis='x', linestyle='--', alpha=0.4)


plt.tight_layout()

# Save the plot
filename = os.path.basename(csv_path)
name_no_ext = os.path.splitext(filename)[0]
output_filename = os.path.join(output_path, f"{name_no_ext}_timeline.png")
plt.savefig(output_filename, dpi=300, bbox_inches='tight')
plt.show()

print(f"Timeline plot saved to: {output_filename}")
print(f"\nTotal seeds: {len(df)}")
print(f"No MF (camera1): {len(df[df['Grid'] == 'camera1'])}")
print(f"MF (camera2): {len(df[df['Grid'] == 'camera2'])}")