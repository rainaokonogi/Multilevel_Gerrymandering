import json
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from pathlib import Path

CURRENT_WORKING_DIRECTORY = Path.cwd()

def accumulate_histogram_vector(file_path, bins):
    """Performs data analysis all block sizes of one fixed grid NN (neutral-neutral) experiment.
    For each plan in each neutral ensemble, finds the number of seats won by the blue party.
    Saves into a numpy array of length 25 (0 to 12 seats, with half-integers)
    where each entry is the number of plans where Dems won that many seats.
    """
        counts = np.zeros(len(bins) - 1, dtype=np.int64)

        with open(file_path, "r") as f:
            for line in tqdm(f, desc=Path(file_path).name):
                data = json.loads(line)
                values = data["Seats_won_D"]
                values = np.array(values)
                counts += np.histogram(values, bins=bins)[0]

        return counts


def make_array(assort_score, num_r_units, map_number):
    """Performs data analysis all block sizes of one fixed grid NN (neutral-neutral) experiment.
    For each plan in each neutral ensemble, finds the number of seats won by the blue party.
    Saves into a numpy array of length 25 (0 to 12 seats, with half-integers)
    where each entry is the number of plans where Dems won that many seats.
    """

    # NN results for all block sizes, other variables fixed
    files = [
        f"{CURRENT_WORKING_DIRECTORY}/REP_DATA/12x12_grid_results/NN/compiled_results/{assort_score}_BR_score_r_units_{num_r_units}_map_{map_number}_block_size_1.jsonl",
        f"{CURRENT_WORKING_DIRECTORY}/REP_DATA/12x12_grid_results/NN/compiled_results/{assort_score}_BR_score_r_units_{num_r_units}_map_{map_number}_block_size_2.jsonl",
        f"{CURRENT_WORKING_DIRECTORY}/REP_DATA/12x12_grid_results/NN/compiled_results/{assort_score}_BR_score_r_units_{num_r_units}_map_{map_number}_block_size_3.jsonl",
        f"{CURRENT_WORKING_DIRECTORY}/REP_DATA/12x12_grid_results/NN/compiled_results/{assort_score}_BR_score_r_units_{num_r_units}_map_{map_number}_block_size_4.jsonl",
        f"{CURRENT_WORKING_DIRECTORY}/REP_DATA/12x12_grid_results/NN/compiled_results/{assort_score}_BR_score_r_units_{num_r_units}_map_{map_number}_block_size_6.jsonl"
    ]

    if not file.exists() for file in files:
        raise FileNotFoundError(
            f"Synthetic results folder not found.\n"
            "This data is available from the author upon request.\n"
        )

    # Output directory for saved histograms
    output_dir = Path(f"{CURRENT_WORKING_DIRECTORY}/fixed_grid_experiment/processed_results_data_(replicated)/neutral_histogram_data")
    output_dir.mkdir(exist_ok=True)

    max_seats = 12
    bins = np.arange(-0.25, max_seats + 0.75, 0.5)

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
    

def main():
    """Performs data analysis for each NN fixed grid experiment.
    """
    for assort_score in ["low", "med", "high"]:
        for num_r_units in ["72", "86"]:
            for map_number in ["1", "2", "3"]:
                make_array(assort_score, num_r_units, map_number)

main()