import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("virtual_field_data.csv")

zones = df["zone"].unique()

for zone in zones:
    zone_data = df[df["zone"] == zone]
    plt.plot(zone_data["soil_moisture"].values)

plt.title("Zone Moisture Over Time")
plt.xlabel("Time Index")
plt.ylabel("Moisture %")
plt.show()