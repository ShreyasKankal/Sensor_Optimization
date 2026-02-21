# virtual_data_generator.py

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Configuration
NUM_ZONES = 5
HOURS = 48
INTERVAL_MINUTES = 30
BASE_MOISTURE = 40

zones = ["A", "B", "C", "D", "E"]

data = []

start_time = datetime.now()

current_moisture = {
    zone: BASE_MOISTURE + np.random.uniform(-5, 5)
    for zone in zones
}

for i in range(int((HOURS * 60) / INTERVAL_MINUTES)):

    timestamp = start_time + timedelta(minutes=i * INTERVAL_MINUTES)

    irrigation = 60 if i % 4 == 0 else 0  # irrigate every 2 hours

    for zone in zones:

        # Natural drying effect
        drying = np.random.uniform(0.2, 0.6)

        # Irrigation effect
        irrigation_effect = irrigation * np.random.uniform(0.03, 0.06)

        current_moisture[zone] = (
            current_moisture[zone]
            - drying
            + irrigation_effect
        )

        current_moisture[zone] = max(20, min(80, current_moisture[zone]))

        data.append([
            timestamp,
            zone,
            round(current_moisture[zone], 2),
            irrigation
        ])

df = pd.DataFrame(
    data,
    columns=["timestamp", "zone", "soil_moisture", "irrigation_seconds"]
)

df.to_csv("virtual_field_data.csv", index=False)

print("Virtual dataset generated: virtual_field_data.csv")