import json
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from tqdm import tqdm

CURRENT_WORKING_DIRECTORY = Path.cwd()

# Configuration
files = [
    f"/share/duchin/raina/REP_DATA/6-12-24_grid_exp/24x24_grid_results/NN_compiled/med_BR_r_units_21_map_1_block_size_1.jsonl",
    f"/share/duchin/raina/REP_DATA/6-12-24_grid_exp/24x24_grid_results/NN_compiled/med_BR_r_units_21_map_1_block_size_2.jsonl",
    f"/share/duchin/raina/REP_DATA/6-12-24_grid_exp/24x24_grid_results/NN_compiled/med_BR_r_units_21_map_1_block_size_3.jsonl"
]

# Max number of seats across all geographies
max_seats = 6
bins = np.arange(-0.25, max_seats + 0.75, 0.5)  # integer bins [0,1), [1,2), ..., [63,64)

# Output directory for saved histograms
output_dir = Path("/share/duchin/raina/REPLICATION_REPO/6-12-24_grid_experiment/processed_results_data/24x24_grid_results/NN")
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