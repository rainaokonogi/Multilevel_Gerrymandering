import os
import json
from tqdm import tqdm
from pathlib import Path

CURRENT_WORKING_DIRECTORY = Path.cwd()

def find_minimums(run_path, out_path):
    """
    Looks at the short bursts optimization runs gerrymandered toward the red party
    and saves, for each chain, the minimum number of seats won by the blue party in any plan.

    Args:
    run_path: path containing results folders for all experiments on one underlying grid
    out_path: file where we'll record all the minimums for experiments on underlying grid
    """

    with open(out_path, "w") as outfile:

        block_folders = sorted(os.listdir(run_path))

        # Loop over block sizes
        for block_folder in tqdm(block_folders, desc="block folders", leave=False):
            block_path = os.path.join(run_path, block_folder)

            min_values = []   # will hold 1500 values

            # For each block size, loop over samples
            # Each sample is a set of experiments using a different building block partition
            sample_folders = [
                sample for sample in os.listdir(block_path)
            ]

            for sample_folder in tqdm(sample_folders, desc=f"{block_folder} samples", leave=False):
                sample_path = os.path.join(block_path, sample_folder)

                # For each sample, loop over experiment results files
                # Each experiment varies the random seed, initial partition
                for exp in os.listdir(sample_path):
                    exp_path = os.path.join(sample_path, exp)

                    file_min = None

                    with open(exp_path) as f:
                        for line in f:
                            if not line.strip(): # skip any blank lines
                                continue
                            try:
                                record = json.loads(line)
                                d = record["Seats won"]["D"]
                                r = record["Seats won"]["R"]
                            except (KeyError, json.JSONDecodeError):
                                continue

                            # For each plan in the chain, compute the number of blue seats, recalling that ties counts as half a seat
                            seats_d = d
                            seats_without_ties = d + r
                            if seats_without_ties != 6:
                                seats_d += 0.5 * (6 - seats_without_ties)

                            # Update min number of blue seats found across the chain as necessary
                            if file_min is None or file_min > seats_d:
                                file_min = seats_d

                    if file_min is not None:
                        min_values.append(file_min)

            # Write 1500 min values per block size per underlying grid
            out_record = {
                "Block size": block_folder,
                "Min Values": min_values
            }

            outfile.write(json.dumps(out_record) + "\n")

    tqdm.write(f"Wrote {out_path}")

def main():
    """
    Performs data analysis of finding min numbers of blue seats
    for all fixed grid experiments gerrymandered toward red.
    """

    for N in [6, 12, 24]:
        BASE_DIR = f"{CURRENT_WORKING_DIRECTORY}/REP_DATA/6-12-24_grid_results/{N}x{N}_grid_results/NG/output_updaters/toward_R/"
        OUT_DIR = Path(f"{CURRENT_WORKING_DIRECTORY}/6-12-24_grid_results/processed_results_data_(replicated)/{N}x{N}_grid_results/NG/NG_minimums")
        os.makedirs(OUT_DIR, exist_ok=True)

        if not os.path.exists(BASE_DIR):
            print("Data is available from the author upon request.")

        run_folders = [
            f for f in os.listdir(BASE_DIR)
            # if f == "med_BR_score_r_units_72_map_1"
            # If you want to speed this up and you are able to run jobs in parallel, you can un-comment out the above line
            # and modify it to kick off separate jobs for each underlying grid.
        ]

        for run_folder in tqdm(run_folders, desc="Run folders"):
            run_path = os.path.join(BASE_DIR, run_folder)
            out_path = os.path.join(OUT_DIR, f"{run_folder}.jsonl")
            find_minimums(run_path, out_path)

main()