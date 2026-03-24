import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ===================== USER SETTINGS =====================
DATA_DIR = r"C:\Users\marik\Documents\000\2025\ScienceResearch_2025_26\Data"
GROUP_SIZES = [10, 10]            # Group 1, Group 2, rest = Group 3
EXPECTED_SEEDS = 21
# ========================================================

# Get all CSV files
csv_files = sorted([
    f for f in os.listdir(DATA_DIR)
    if f.lower().endswith(".csv")
])

# Split files into groups
groups = []
start = 0
for size in GROUP_SIZES:
    groups.append(csv_files[start:start + size])
    start += size
groups.append(csv_files[start:])  # Remaining files

def analyze_group(file_list, group_name):
    cam1_missing = []
    cam2_missing = []

    for filename in file_list:
        path = os.path.join(DATA_DIR, filename)
        df = pd.read_csv(path)

        cam1_count = len(df[df["Grid"] == "camera1"])
        cam2_count = len(df[df["Grid"] == "camera2"])

        cam1_missing.append(EXPECTED_SEEDS - cam1_count)
        cam2_missing.append(EXPECTED_SEEDS - cam2_count)

    avg_cam1 = sum(cam1_missing) / len(cam1_missing)
    avg_cam2 = sum(cam2_missing) / len(cam2_missing)

    # Plot
    plt.figure()
    plt.bar(["Camera 1", "Camera 2"], [avg_cam1, avg_cam2])
    plt.ylabel("Average Missing Seeds")
    plt.title(group_name)
    plt.show()

# Run analysis
for i, group_files in enumerate(groups, start=1):
    if not group_files:
        continue
    analyze_group(group_files, f"Group {i}")
