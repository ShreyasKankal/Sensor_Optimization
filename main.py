from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np

app = FastAPI()

# Allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change later for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/spatial-analysis")
def spatial_analysis():

    df = pd.read_csv("virtual_field_data.csv")

    results = []

    for timestamp in df["timestamp"].unique():
        temp = df[df["timestamp"] == timestamp]
        values = temp["soil_moisture"].values

        mean = np.mean(values)
        std = np.std(values)

        if mean == 0:
            continue

        cv = (std / mean) * 100
        results.append(cv)

    average_cv = np.mean(results)

    if average_cv < 10:
        recommendation = "Field is uniform → 1-2 sensors sufficient."
    elif average_cv < 20:
        recommendation = "Moderate variability → 3-5 sensors recommended."
    else:
        recommendation = "High variability → 5+ sensors required."

    return {
        "average_cv": round(float(average_cv), 2),
        "recommendation": recommendation
    }