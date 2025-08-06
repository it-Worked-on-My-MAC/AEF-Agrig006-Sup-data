#!/usr/bin/env python3
import sys
import pandas as pd
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.spatial.distance import squareform
import re

# The script now expects paths as command line arguments
file_path = sys.argv[1]
output_png = sys.argv[2]
output_pdf = sys.argv[3]

# === Load file ===
print(f"Reading: {file_path}")
df = pd.read_csv(file_path, sep='\t', header=None,
                 names=['Sample1', 'Sample2', 'Distance', 'Pvalue', 'SharedHashes'])

# === Extract numeric sample ID from paths ===
def extract_id(path):
    match = re.search(r"/(\d+)_spades/", path)
    return match.group(1) if match else path

df['Sample1'] = df['Sample1'].apply(extract_id)
df['Sample2'] = df['Sample2'].apply(extract_id)

# === Create symmetric distance matrix ===
print("Creating distance matrix...")
dist_matrix = df.pivot(index='Sample1', columns='Sample2', values='Distance').fillna(0)
dist_matrix = dist_matrix.reindex(sorted(dist_matrix.columns), axis=1).reindex(sorted(dist_matrix.columns), axis=0)
dist_matrix = (dist_matrix + dist_matrix.T) / 2 # Force symmetry

# === Linkage calculation ===
print("Calculating linkage matrix...")
condensed_dist = squareform(dist_matrix.values)
linkage_matrix = linkage(condensed_dist, method='average')

# === Group assignment logic ===
alt_germany = {"5", "10"}
alt_serbia = {"47", "62"}
germany = {"2", "8"}
serbia = {"20", "24", "25", "26", "34", "35", "37", "38", "54", "56", "58", "59", "60", "64", "66", "73", "79", "80", "82", "89"}
algeria = {"96", "116"}

def assign_group(sample_id):
    if sample_id in alt_germany:
        return "A. alternata - Germany"
    elif sample_id in alt_serbia:
        return "A. alternata - Serbia"
    elif sample_id in germany:
        return "Sus A. Arborescens - Germany"
    elif sample_id in serbia:
        return "Sus A. Arborescens - Serbia"
    elif sample_id in algeria:
        return "Sus A. Arborescens - Algeria"
    else:
        return "Sus A. Arborescens - Unknown"

# === Build labels with group names ===
print("Assigning group labels...")
sample_order = dist_matrix.index.tolist()
new_labels = [f"{sid} ({assign_group(sid)})" for sid in sample_order]

# === Plot dendrogram ===
print("Plotting dendrogram...")
plt.figure(figsize=(14, 8))
dendrogram(linkage_matrix, labels=new_labels, leaf_rotation=90)
plt.title("Mash Distance Dendrogram with Subgrouping")
plt.xlabel("Sample ID (Group)")
plt.ylabel("Mash Distance")
plt.tight_layout()

# === Save outputs ===
plt.savefig(output_png)
plt.savefig(output_pdf)
print(f"Saved:\n- {output_png}\n- {output_pdf}")
plt.show()