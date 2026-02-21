import pandas as pd
import numpy as np

df = pd.read_csv("virtual_field_data.csv")

zones = df["zone"].unique()

# ---- Calculate Average CV ----
cv_list = []

for timestamp in df["timestamp"].unique():
    temp = df[df["timestamp"] == timestamp]
    values = temp["soil_moisture"].values
    mean = np.mean(values)
    std = np.std(values)
    cv = (std / mean) * 100
    cv_list.append(cv)

average_cv = np.mean(cv_list)

print("Average CV:", round(average_cv, 2), "%")

# ---- Zone Deviation Detection ----
zone_deviation = {zone: [] for zone in zones}

for timestamp in df["timestamp"].unique():
    temp = df[df["timestamp"] == timestamp]
    mean = temp["soil_moisture"].mean()
    
    for zone in zones:
        value = temp[temp["zone"] == zone]["soil_moisture"].values[0]
        zone_deviation[zone].append(abs(value - mean))

avg_dev = {zone: np.mean(zone_deviation[zone]) for zone in zones}

print("\nZone Average Deviations:")
for zone, dev in avg_dev.items():
    print(zone, ":", round(dev, 2))

overall_std = np.std(list(avg_dev.values()))

print("\nMandatory Zones:")
for zone, dev in avg_dev.items():
    if dev > 1.5 * overall_std:
        print(zone, "must have independent sensor")