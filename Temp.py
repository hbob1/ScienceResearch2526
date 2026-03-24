import os
import csv
from datetime import datetime
import matplotlib.pyplot as plt
from sympy.printing.pretty.pretty_symbology import line_width

TXT_DIR = r"C:\Users\marik\Documents\20260113"
KESTREL_CSV = r"C:\Users\marik\Documents\20260113\WEATHER - 2999158_2026-01-16 00_00_00.csv"
OUTPUT_DIR = r"C:\Users\marik\Documents\000\2025\ScienceResearch_2025_26\temporary"

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

SENSOR_1 = "28-000000b946f3" # Cam 1 No MF Control
SENSOR_2 = "28-000000b1c3ff" # MF

times_kestrel = []
temps_kestrel = []

with open(KESTREL_CSV, newline="") as f:
    reader = csv.reader(f)

    for row in reader:
        if not row or row[0] in ("Time", "") or row[0].startswith("yyyy"):
            continue
        if row[0].startswith("Device") or row[0].startswith("Name"):
            continue

        try:
            timestamp = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
        except ValueError:
            continue

        try:
            temp = float(row[1])
        except (ValueError, IndexError):
            continue

        times_kestrel.append(timestamp)
        temps_kestrel.append(temp)

times_txt = []
temps_1 = []
temps_2 = []

for filename in sorted(os.listdir(TXT_DIR)):
    if not filename.endswith(".txt"):
        continue

    with open(os.path.join(TXT_DIR, filename)) as f:
        lines = f.readlines()

    timestamp_str = lines[0].split(":")[1].strip()
    timestamp = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")

    if timestamp <= times_kestrel[0]:
        continue
    t1 = t2 = None

    for line in lines[1:]:
        if SENSOR_1 in line:
            value = line.split(":")[1]
            t1 = float("".join(c for c in value if c.isdigit() or c == "."))
        elif SENSOR_2 in line:
            value = line.split(":")[1]
            t2 = float("".join(c for c in value if c.isdigit() or c == "."))

    if t1 is not None and t2 is not None:
        times_txt.append(timestamp)
        temps_1.append(t1)
        temps_2.append(t2)

start_time = times_kestrel[0]

start_m = ((temps_kestrel[0] - temps_kestrel[1])/
           ((times_kestrel[0] - times_kestrel[1]).total_seconds()))

start_b = temps_kestrel[1] - (start_m * (times_kestrel[0] - times_kestrel[1]).total_seconds())

kestrel_temp_at_sensor_time = (start_m * (times_kestrel[0] - times_txt[0]).total_seconds()) + start_b

bias_sensor1 = kestrel_temp_at_sensor_time - temps_1[0]
bias_sensor2 = kestrel_temp_at_sensor_time - temps_2[0]

if temps_1 and temps_kestrel:
    temps_1 = [i + bias_sensor1 for i in temps_1]

if temps_2 and temps_kestrel:
    temps_2 = [j + bias_sensor2 for j in temps_2]

while times_kestrel and times_kestrel[-1] > times_txt[-1]:
    times_kestrel.pop()
    temps_kestrel.pop()

# Convert times to hours since experiment start
hours_txt = [(t - start_time).total_seconds() / 3600 for t in times_txt]
hours_kestrel = [(t - start_time).total_seconds() / 3600 for t in times_kestrel]

fig, (ax1, ax2) = plt.subplots(
    2, 1, figsize=(10, 7), sharex=True,
    gridspec_kw={"height_ratios": [2, 1]}
)

# --- Top: Temperatures ---
ax1.plot(hours_txt, temps_1, label="No MF", linewidth=3)
ax1.plot(hours_txt, temps_2, label="MF", linewidth=3)
ax1.plot(hours_kestrel, temps_kestrel, label="Ambient", linewidth=3)

ax1.set_ylabel("Temperature (°C)")
ax1.legend()
ax1.grid(True)

# --- Bottom: Difference ---
temp_diff = [t1 - t2 for t1, t2 in zip(temps_1, temps_2)]

ax2.plot(hours_txt, temp_diff, label="No MF - MF", linewidth=3, color='black')
ax2.axhline(0, linestyle="--", linewidth=2, color='black')

ax2.set_ylabel("ΔT (°C)")
ax2.set_xlabel("Time Since Experiment Start (hours)")
ax2.legend()
ax2.grid(True)

plt.tight_layout()

# Extract date from the TXT_DIR folder name or from first timestamp
# Using the folder name (e.g., "20251112")
date_str = os.path.basename(TXT_DIR)

# Save the plot
output_filename = os.path.join(OUTPUT_DIR, f"{date_str}_TEMP.png")
plt.savefig(output_filename, dpi=300, bbox_inches='tight')
print(f"Plot saved to: {output_filename}")
print(f"Experiment start time: {start_time}")
print(f"Duration: {hours_txt[-1]:.1f} hours")

plt.show()