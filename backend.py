from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import math
import random

app = FastAPI()

# Allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# your routes below
@app.get("/")
def read_root():
    return {"message": "Hello"}

# Request model
class FarmRequest(BaseModel):
    farm_size: float  # hectares


@app.post("/spatial-analysis")
def spatial_analysis(data: FarmRequest):

    farm_size = data.farm_size

    # -----------------------------
    # 1️⃣ Generate Realistic Soil Data
    # -----------------------------

    zones = max(8, int(farm_size * 2))  # more zones for bigger farms
    timestamps = 10

    base_moisture = random.uniform(35, 55)

    moisture_values = []

    for t in range(timestamps):
        for zone in range(zones):

            # Spatial gradient (field heterogeneity)
            spatial_effect = np.sin(zone / zones * np.pi) * random.uniform(3, 8)

            # Temporal fluctuation (weather/irrigation changes)
            temporal_effect = random.uniform(-4, 4)

            moisture = base_moisture + spatial_effect + temporal_effect

            # Keep values realistic
            moisture = max(15, min(80, moisture))

            moisture_values.append(moisture)

    soil_moisture = np.array(moisture_values)

    # -----------------------------
    # 2️⃣ Compute Spatial Variability
    # -----------------------------

    mean = np.mean(soil_moisture)
    std = np.std(soil_moisture)
    cv = (std / mean) * 100

    # -----------------------------
    # 3️⃣ Dynamic Sensor Calculation
    # -----------------------------

    # Sensor density grows with variability + farm size
    variability_factor = cv / 10
    size_factor = math.sqrt(farm_size)

    sensor_count = math.ceil(size_factor * variability_factor * 1.2)

    # Minimum safety constraint
    sensor_count = max(sensor_count, 1)

    # -----------------------------
    # 4️⃣ Smart Recommendation Text
    # -----------------------------

    if cv < 10:
        field_type = "Uniform Field"
    elif cv < 20:
        field_type = "Moderately Variable Field"
    else:
        field_type = "Highly Variable Field"

    recommendation = (
        f"{sensor_count} sensors recommended for optimal coverage. "
        f"The field shows {field_type} characteristics with a CV of {round(cv,2)}%."
    )

    # -----------------------------
    # 5️⃣ Return Response
    # -----------------------------

    return {
        "average_cv": round(float(cv), 2),
        "sensor_count": sensor_count,
        "recommendation": recommendation
    }