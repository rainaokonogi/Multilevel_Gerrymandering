import os
import json
import csv
from pathlib import Path

CURRENT_WORKING_DIRECTORY = Path.cwd()

def main():
    """
    Compiles NN results into a more usable format.
    Specifically, instead of having an individual file for each neutral ReCom chain, creates one file for each grid on which we ran the experiment.
    In that file, each line represents one of the 100 samples (i.e., set of 15 experiments run with one building block experiment).
    Each line stores a list of every number of seats won by blue in every plan in each of those 15 experiments.
    """    

    BASE_DIR = f"{CURRENT_WORKING_DIRECTORY}/REP_DATA/12x12_grid_results/NN/output_updaters/"
    OUT_DIR = f"{CURRENT_WORKING_DIRECTORY}/fixed_grid_experiment/fixed_grid_results_(replicated)/NN/compiled_results/"
    os.makedirs(OUT_DIR, exist_ok=True)

    if not os.path.exists(BASE_DIR):
        print("Data is available from the author upon request.")

    # Iterate over all NN experiments for the different grids
    for grid_folder in os.listdir(BASE_DIR):
        grid_path = os.path.join(BASE_DIR, grid_folder)

        # For each grid, iterate over results for all different block sizes
        for block_size_folder in os.listdir(grid_path):
            block_size_path = os.path.join(grid_path, block_size_folder)

            out_name = f"{grid_folder}_{block_size_folder}.jsonl"
            out_path = os.path.join(OUT_DIR, out_name)

            with open(out_path, "w") as outfile:

                # For each block size, iterate over results for all samples (different building block partitions)
                for sample_folder in os.listdir(block_size_path):
                    sample_path = os.path.join(block_size_path, sample_folder)

                    # Inside the sample folder, look at each results file
                    # For every line in every results file, find the number of seats won by blue (including ties) and append to a list
                    seats_list = []

                    for results_file_name in os.listdir(sample_path):

                        results_file_path = os.path.join(sample_path, results_file_name)

                        with open(results_file_path) as f:
                            for line in f:
                                record = json.loads(line)
                                seats_d = record["Seats won"]["D"]
                                seats_without_ties = record["Seats won"]["D"] + record["Seats won"]["R"]
                                if seats_without_ties != 12:
                                    seats_d = seats_d + 0.5*(12 - seats_without_ties)
                                seats_list.append(seats_d)

                    # Write to compiled file
                    out_record = {
                        "sample": sample_folder,
                        "Seats_won_D": seats_list
                    }

                    outfile.write(json.dumps(out_record) + "\n")

            print(f"Wrote {out_path}")

main()