#!/usr/bin/env python3
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.spatial.distance import squareform

# The script now expects paths as command line arguments
input_file = sys.argv[1]
output_pdf = sys.argv[2]

# === Load and Prepare Data ===
df = pd.read_csv(input_file, sep='\t')

# Build ANI matrix
ani_matrix = df.pivot(index='Query', columns='Reference', values='ANI')

# Fill diagonal with 100
for sample in ani_matrix.index:
    ani_matrix.loc[sample, sample] = 100

# Make symmetric and fill missing values
ani_matrix = ani_matrix.combine_first(ani_matrix.T)
ani_matrix = ani_matrix.fillna(0)
ani_matrix = (ani_matrix + ani_matrix.T) / 2

# Convert ANI to distance (100 - ANI)
distance_matrix = 100 - ani_matrix

# Convert to condensed format for linkage
condensed_dist = squareform(distance_matrix)

# Perform clustering
Z = linkage(condensed_dist, method='average')

# === Define group labels ===
group_map = {
    '5': 'A. alternata: Germany',
    '10': 'A. alternata: Germany',
    '47': 'A. alternata: Serbia',
    '62': 'A. alternata: Serbia',
    '2': 'Sus A. arborescens: Germany',
    '8': 'Sus A. arborescens: Germany',
    '20': 'Sus A. arborescens: Serbia',
    '24': 'Sus A. arborescens: Serbia',
    '25': 'Sus A. arborescens: Serbia',
    '26': 'Sus A. arborescens: Serbia',
    '35': 'Sus A. arborescens: Serbia',
    '37': 'Sus A. arborescens: Serbia',
    '38': 'Sus A. arborescens: Serbia',
    '54': 'Sus A. arborescens: Serbia',
    '56': 'Sus A. arborescens: Serbia',
    '58': 'Sus A. arborescens: Serbia',
    '59': 'Sus A. arborescens: Serbia',
    '64': 'Sus A. arborescens: Serbia',
    '66': 'Sus A. arborescens: Serbia',
    '73': 'Sus A. arborescens: Serbia',
    '79': 'Sus A. arborescens: Serbia',
    '80': 'Sus A. arborescens: Serbia',
    '82': 'Sus A. arborescens: Serbia',
    '89': 'Sus A. arborescens: Serbia',
    '96': 'Sus A. arborescens: Algeria',
    '116': 'Sus A. arborescens: Algeria'
}

def label_with_group(sample_id):
    group = group_map.get(str(sample_id), "Unknown")
    return f"{sample_id} ({group})"

labels_with_groups = [label_with_group(s) for s in ani_matrix.index]

# Plot dendrogram with labeled leaves
plt.figure(figsize=(12, 6))
dendrogram(Z, labels=labels_with_groups, leaf_rotation=90, leaf_font_size=10)
plt.title("Hierarchical Clustering Dendrogram (FastANI Distance)")
plt.ylabel("Distance (100 - ANI)")
plt.tight_layout()

plt.savefig(output_pdf)
plt.show()
print(f"✅ Dendrogram saved to {output_pdf}")