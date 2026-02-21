from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np

app = FastAPI()

# Allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://sensor-lab-pro.vercel.app"], # Better to be specific!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Define what the incoming data looks like
class AnalysisRequest(BaseModel):
    value: int  # This matches the "800" or "10" from your input box

@app.post("/spatial-analysis")
def spatial_analysis(request: AnalysisRequest): # 2. Accept the request body

    df = pd.read_csv("virtual_field_data.csv")
    
    # 3. Use the input! 
    # For example: Only analyze the last 'n' records based on user input
    # Or filter by a specific range.
    subset = df.head(request.value) 

    results = []
    for timestamp in subset["timestamp"].unique():
        temp = subset[subset["timestamp"] == timestamp]
        values = temp["soil_moisture"].values
        mean = np.mean(values)
        std = np.std(values)

        if mean == 0:
            continue

        cv = (std / mean) * 100
        results.append(cv)

    average_cv = np.mean(results) if results else 0

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