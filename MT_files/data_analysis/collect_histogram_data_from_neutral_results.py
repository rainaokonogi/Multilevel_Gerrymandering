from pathlib import Path
import numpy as np
import json
from tqdm import tqdm
import os

CURRENT_WORKING_DIRECTORY = Path.cwd()

dir_paths = {
    "blockgroups": Path(f"{CURRENT_WORKING_DIRECTORY}/MT_results/neutral_output_updaters/blockgroups")
    "tracts": Path(f"{CURRENT_WORKING_DIRECTORY}/MT_results/neutral_output_updaters/tracts")
    "vtds": Path(f"{CURRENT_WORKING_DIRECTORY}/MT_results/neutral_output_updaters/vtds")
}

for units, units_path in dir_paths.items():
    if not units_path.exists():
        raise FileNotFoundError(
            f"Montana {units} results file not found.\n"
            "This data is available from the author upon request.\n"
        )

max_seats = 50
bins = np.arange(0, 52, 1)

output_dir = f"{CURRENT_WORKING_DIRECTORY}/REPLICATION_REPO/MT_data_analysis_replicated/neutral_histogram_data/"
os.makedirs(output_dir, exist_ok=True)

def accumulate_histogram(dir_path, bins):
    counts = np.zeros(len(bins) - 1)

    files = list(dir_path.glob("*.jsonl"))

    for file_path in tqdm(files, desc=f"{dir_path.name} files", total=len(files)):
        with open(file_path, "r") as f:
            for line in tqdm(f, desc=f"{file_path.name}", leave=False):
                data = json.loads(line)
                values = np.array(data["Pres seats won"]["D"])
                counts += np.histogram(values, bins=bins)[0]

    return counts

# Compute one histogram per directory
histograms = {}

for name, dir_path in dir_paths.items():
    print(f"\nProcessing directory: {name}")
    histograms[name] = accumulate_histogram_for_directory(dir_path, bins)

# Save results (3 files total)
for name, counts in histograms.items():
    out_path = output_dir + f"{name}_pres_histogram.npy"
    np.save(out_path, counts)
    print(f"Saved: {out_path}")