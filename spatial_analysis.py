# spatial_analysis.py

import pandas as pd
import numpy as np

df = pd.read_csv("virtual_field_data.csv")

results = []

for timestamp in df["timestamp"].unique():

    temp = df[df["timestamp"] == timestamp]
    values = temp["soil_moisture"].values

    mean = np.mean(values)
    variance = np.var(values)
    std = np.std(values)
    cv = (std / mean) * 100

    results.append([timestamp, mean, variance, std, cv])

analysis = pd.DataFrame(
    results,
    columns=["timestamp", "mean", "variance", "std_dev", "cv_percent"]
)

analysis.to_csv("spatial_variance_analysis.csv", index=False)

average_cv = analysis["cv_percent"].mean()

print("Average CV:", round(average_cv, 2), "%")

# Sensor recommendation logic
if average_cv < 10:
    recommendation = "Field is uniform → 1-2 sensors sufficient."
elif 10 <= average_cv < 20:
    recommendation = "Moderate variability → 3-5 sensors recommended."
else:
    recommendation = "High variability → 5+ sensors required."

print("Recommendation:", recommendation)