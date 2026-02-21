import pandas as pd
import numpy as np

def perform_spatial_analysis(limit: int):
    # Load the data
    try:
        df = pd.read_csv("virtual_field_data.csv")
    except FileNotFoundError:
        return {"error": "Data file not found"}

    # Use the input to subset the data (Dynamic Analysis)
    # We take the last 'limit' records to show recent trends
    subset = df.tail(limit) 

    results = []
    for timestamp in subset["timestamp"].unique():
        temp = subset[subset["timestamp"] == timestamp]
        values = temp["soil_moisture"].values
        
        if len(values) == 0:
            continue
            
        mean = np.mean(values)
        std = np.std(values)

        if mean == 0:
            continue

        cv = (std / mean) * 100
        results.append(cv)

    if not results:
        return {"average_cv": 0, "recommendation": "No data available for this range."}

    average_cv = np.mean(results)

    if average_cv < 10:
        recommendation = "Field is uniform → 1-2 sensors sufficient."
    elif average_cv < 20:
        recommendation = "Moderate variability → 3-5 sensors recommended."
    else:
        recommendation = "High variability → 5+ sensors required."

    return {
        "average_cv": round(float(average_cv), 2),
        "recommendation": recommendation,
        "data_points_analyzed": len(subset)
    }