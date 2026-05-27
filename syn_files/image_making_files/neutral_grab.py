import json
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from tqdm import tqdm

# Configuration
files = [
    "/share/duchin/raina/output_stats/new_score_function/NN_ensembles_new/high_BR_score_r_units_72_map_3_block_size_1.jsonl",
    "/share/duchin/raina/output_stats/new_score_function/NN_ensembles_new/high_BR_score_r_units_72_map_3_block_size_2.jsonl",
    "/share/duchin/raina/output_stats/new_score_function/NN_ensembles_new/high_BR_score_r_units_72_map_3_block_size_3.jsonl",
    "/share/duchin/raina/output_stats/new_score_function/NN_ensembles_new/high_BR_score_r_units_72_map_3_block_size_4.jsonl",
    "/share/duchin/raina/output_stats/new_score_function/NN_ensembles_new/high_BR_score_r_units_72_map_3_block_size_6.jsonl"
]

# Max number of seats across all geographies
max_seats = 12
bins = np.arange(-0.25, max_seats + 0.75, 0.5)  # integer bins [0,1), [1,2), ..., [63,64)

# Output directory for saved histograms
output_dir = Path("./saved_histograms_2")
output_dir.mkdir(exist_ok=True)

# Function to accumulate histogram counts per folder
def accumulate_histogram_vector(file_path, bins):
    counts = np.zeros(len(bins) - 1, dtype=np.int64)

    # Vectorized read
    with open(file_path, "r") as f:
        for line in tqdm(f, desc=Path(file_path).name):
            data = json.loads(line)
            values = data["Seats_won_D"]
            values = np.array(values)
            counts += np.histogram(values, bins=bins)[0]

    print(counts)
    return counts

# Process all folders
histograms = {}
for file_path in files:
    key = Path(file_path).name
    print(key)
    print(f"\nProcessing {key} ...")
    histograms[key] = accumulate_histogram_vector(file_path, bins)

# Save histograms and bins
print(histograms.keys())
for key, counts in histograms.items():
    np.save(output_dir / f"{key}_histogram.npy", counts)
print(f"\nSaved histogram counts and bins to {output_dir}")