from pathlib import Path
import numpy as np
import json
from tqdm import tqdm
import os

print("CWD IS:", os.getcwd())
print("OUTPUT DIR RESOLVED:", Path("./saved_histograms_2").resolve())

# Configuration
dir_paths = {
    "blockgroups": Path("/share/duchin/raina/REPLICATION_REPO/MT_results/neutral_output_updaters/blockgroups")
    # "tracts": Path("/share/duchin/raina/REPLICATION_REPO/MT_results/neutral_output_updaters/tracts")
    # "vtds": Path("/share/duchin/raina/REPLICATION_REPO/MT_results/neutral_output_updaters/vtds")
}

max_seats = 50
bins = np.arange(0, 52, 1)

output_dir = f"/share/duchin/raina/REPLICATION_REPO/MT_files/saved_hists_MT/"
os.makedirs(output_dir, exist_ok=True)

def accumulate_histogram_for_directory(dir_path, bins):
    counts = np.zeros(len(bins) - 1)

    files = list(dir_path.glob("*.jsonl"))
    print(f"{dir_path.name}: {len(files)} files")

    for file_path in tqdm(files, desc=f"{dir_path.name} files", total=len(files)):
        with open(file_path, "r") as f:
            for line in tqdm(f, desc=f"{file_path.name}", leave=False):
                data = json.loads(line)
                values = np.array(data["Pres seats won"]["D"])
                counts += np.histogram(values, bins=bins)[0]

        print(counts)
        print(len(counts))
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

print("\nDone. Saved 3 aggregated histograms.")