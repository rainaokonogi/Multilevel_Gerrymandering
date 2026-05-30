from pathlib import Path
import numpy as np
import json
from tqdm import tqdm
import os

CURRENT_WORKING_DIRECTORY = Path.cwd()

def main():
    """Performs data analysis on the neutral New York experiment results.
    For each plan in each neutral ensemble, finds the number of seats won by Democrats using Sen2020 data.
    Saves into a numpy array of length 51 (0 to 50 seats) where each entry is the number of plans where Dems won that many seats.
    Does this for each of the three types of census units.
    """

    dir_paths = {
        "vtds": Path(f"{CURRENT_WORKING_DIRECTORY}/REP_DATA/Montana_results/neutral/neutral_updaters/vtds"),
        "blockgroups": Path(f"{CURRENT_WORKING_DIRECTORY}/REP_DATA/Montana_results/neutral/neutral_updaters/blockgroups"),
        "tracts": Path(f"{CURRENT_WORKING_DIRECTORY}/REP_DATA/Montana_results/neutral/neutral_updaters//tracts")
    }

    for units, units_path in dir_paths.items():
        if not units_path.exists():
            raise FileNotFoundError(
                f"Montana {units} results file not found.\n"
                "This data is available from the author upon request.\n"
            )

    output_dir = f"{CURRENT_WORKING_DIRECTORY}/MT_files/processed_results_data_(replicated)/neutral_histogram_data/"
    os.makedirs(output_dir, exist_ok=True)

    def accumulate_histogram(dir_path):
    """Creates a numpy array of length 51 where each entry counts the number of plans across ensembles where Dems won that many seats.

    Args:
        dir_path: Path for folder containing all .jsonl files for MT neutral runs for one census unit.
    """

        # We want length 52, since that creates an array 0-1, 1-2, ..., 50-51.
        bins = np.arange(0, 52, 1)
        counts = np.zeros(len(bins) - 1)

        files = list(dir_path.glob("*.jsonl"))

        # For each plan in each file, add number of seats won by Dems to totals
        for file_path in tqdm(files, desc=f"{dir_path.name} files", total=len(files)):
            with open(file_path, "r") as f:
                for line in tqdm(f, desc=f"{file_path.name}", leave=False):
                    data = json.loads(line)
                    values = np.array(data["Sen seats won"]["D"])
                    counts += np.histogram(values, bins=bins)[0]

        return counts

    # Compute one histogram for each type of census unit
    histograms = {}

    for name, dir_path in dir_paths.items():
        print(f"\nProcessing directory: {name}")
        histograms[name] = accumulate_histogram_for_directory(dir_path)

    # Save results (3 files total)
    for name, counts in histograms.items():
        out_path = output_dir + f"neutral_sen_{name}_histogram.npy"
        np.save(out_path, counts)
        print(f"Saved: {out_path}")

main()