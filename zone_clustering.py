import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# Load data
df = pd.read_csv("virtual_field_data.csv")
zones = df["zone"].unique()

# Build zone matrix (time series per zone)
zone_matrix = []

for zone in zones:
    zone_series = df[df["zone"] == zone]["soil_moisture"].values
    zone_matrix.append(zone_series)

zone_matrix = np.array(zone_matrix)

# -------- Find Optimal Cluster Count --------
sil_scores = []

for k in range(2, len(zones)):
    kmeans = KMeans(n_clusters=k, random_state=42)
    labels = kmeans.fit_predict(zone_matrix)
    score = silhouette_score(zone_matrix, labels)
    sil_scores.append((k, score))

optimal_k = max(sil_scores, key=lambda x: x[1])[0]

print("Optimal number of clusters (sensors):", optimal_k)

# -------- Final Clustering --------
kmeans = KMeans(n_clusters=optimal_k, random_state=42)
labels = kmeans.fit_predict(zone_matrix)

cluster_groups = {}

for zone, label in zip(zones, labels):
    cluster_groups.setdefault(label, []).append(zone)

print("\nZone Clusters:")
for cluster, members in cluster_groups.items():
    print("Cluster", cluster+1, ":", members)

print("\nRecommended Sensor Placement:")
for cluster, members in cluster_groups.items():
    print("Place sensor in:", members[0], "→ covers", members)