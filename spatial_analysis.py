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
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 👇 Request model
class FarmRequest(BaseModel):
    farm_size: int


@app.post("/spatial-analysis")
def spatial_analysis(data: FarmRequest):

    farm_size = data.farm_size

    # Simulate soil moisture grid based on farm size
    num_points = farm_size * 5   # more size → more data points
    soil_moisture = np.random.normal(
        loc=30,                 # average moisture
        scale=farm_size / 20,   # variability increases with size
        size=num_points
    )

    mean = np.mean(soil_moisture)
    std = np.std(soil_moisture)
    cv = (std / mean) * 100

    if cv < 10:
        recommendation = "Field is uniform → 1-2 sensors sufficient."
    elif cv < 20:
        recommendation = "Moderate variability → 3-5 sensors recommended."
    else:
        recommendation = "High variability → 5+ sensors required."

    return {
        "average_cv": round(float(cv), 2),
        "recommendation": recommendation
    }