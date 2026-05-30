import json
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from tqdm import tqdm

CURRENT_WORKING_DIRECTORY = Path.cwd()

def main(assort_score, num_r_units, map_number):
    """Performs data analysis on the neutral main grid experiment results.
    For each plan in each neutral ensemble, finds the number of seats won by the blue party.
    Saves into a numpy array of length 25 (0 to 12 seats, with half-integers)
    where each entry is the number of plans where Dems won that many seats.
    Does this for each of block size.
    """

    files = [
        f"{CURRENT_WORKING_DIRECTORY}/REP_DATA/12x12_grid_results/NN/{assort_score}_BR_score_r_units_{num_r_units}_map_{map_number}_block_size_1.jsonl",
        f"{CURRENT_WORKING_DIRECTORY}/REP_DATA/12x12_grid_results/NN/{assort_score}_BR_score_r_units_{num_r_units}_map_{map_number}_block_size_2.jsonl",
        f"{CURRENT_WORKING_DIRECTORY}/REP_DATA/12x12_grid_results/NN/{assort_score}_BR_score_r_units_{num_r_units}_map_{map_number}_block_size_3.jsonl",
        f"{CURRENT_WORKING_DIRECTORY}/REP_DATA/12x12_grid_results/NN/{assort_score}_BR_score_r_units_{num_r_units}_map_{map_number}_block_size_4.jsonl",
        f"{CURRENT_WORKING_DIRECTORY}/REP_DATA/12x12_grid_results/NN/{assort_score}_BR_score_r_units_{num_r_units}_map_{map_number}_block_size_6.jsonl"
    ]

    if not file.exists() for file in files:
        raise FileNotFoundError(
            f"Synthetic results folder not found.\n"
            "This data is available from the author upon request.\n"
        )

    # Max number of seats across all geographies
    max_seats = 12
    bins = np.arange(-0.25, max_seats + 0.75, 0.5)  # integer bins [0,1), [1,2), ..., [63,64)

    # Output directory for saved histograms
    output_dir = Path(f"{CURRENT_WORKING_DIRECTORY}/main_grid_experiment/processed_results_data_(replicated)/neutral_histograms")
    output_dir.mkdir(exist_ok=True)

    # Function to accumulate histogram counts per folder
    def accumulate_histogram_vector(file_path, bins):
        counts = np.zeros(len(bins) - 1, dtype=np.int64)

        with open(file_path, "r") as f:
            for line in tqdm(f, desc=Path(file_path).name):
                data = json.loads(line)
                values = data["Seats_won_D"]
                values = np.array(values)
                counts += np.histogram(values, bins=bins)[0]

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

for assort_score in ["low", "med", "high"]:
    for num_r_units in ["72", "86"]:
        for map_number in ["1", "2", "3"]:
            main(assort_score, num_r_units, map_number)