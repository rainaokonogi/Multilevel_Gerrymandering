import os
import json
from tqdm import tqdm

BASE_DIR = "/share/duchin/raina/REP_DATA/6-12-24_grid_results/12x12_grid_results/NG/output_updaters/toward_R/"
OUT_DIR = "/share/duchin/raina/REPLICATION_REPO/6-12-24_grid_experiment/processed_results_data/12x12_grid_results/NG/NG_minimums"
os.makedirs(OUT_DIR, exist_ok=True)

run_folders = [
    f for f in os.listdir(BASE_DIR)
    if f == "med_BR_r_units_21_map_1"
]

for run_folder in tqdm(run_folders, desc="Run folders"):

    run_path = os.path.join(BASE_DIR, run_folder)
    if not os.path.isdir(run_path):
        continue

    # one output per r_units_X_map_Y
    out_path = os.path.join(OUT_DIR, f"{run_folder}.jsonl")

    with open(out_path, "w") as outfile:

        block_folders = sorted(os.listdir(run_path))

        # loop over block sizes
        for block_folder in tqdm(block_folders, desc=f"{run_folder} blocks", leave=False):
            block_path = os.path.join(run_path, block_folder)
            if not os.path.isdir(block_path):
                continue

            min_values = []   # will hold 1500 numbers

            # loop over samples
            sample_folders = [
                s for s in os.listdir(block_path)
                if os.path.isdir(os.path.join(block_path, s))
            ]

            for sample_folder in tqdm(sample_folders, desc=f"{block_folder} samples", leave=False):
                sample_path = os.path.join(block_path, sample_folder)
                if not os.path.isdir(sample_path):
                    continue

                # loop over updater files
                for fname in os.listdir(sample_path):
                    if not (
                        fname.startswith("init_part_")
                        and "steps_20000" in fname
                        and fname.endswith("_updaters.jsonl")
                    ):
                        continue

                    fpath = os.path.join(sample_path, fname)

                    file_min = None

                    with open(fpath) as f:
                        for line in f:
                            if not line.strip():
                                continue
                            try:
                                record = json.loads(line)
                                d = record["Seats won"]["D"]
                                r = record["Seats won"]["R"]
                            except (KeyError, json.JSONDecodeError):
                                continue

                            seats_d = d
                            seats_without_ties = d + r
                            if seats_without_ties != 6:
                                seats_d += 0.5 * (6 - seats_without_ties)

                            if file_min is None or file_min > seats_d:
                                file_min = seats_d

                    if file_min is not None:
                        min_values.append(file_min)

            # should be 1500 = 100 * 15
            tqdm.write(f"{run_folder} | {block_folder} count = {len(min_values)}")

            out_record = {
                "Block size": block_folder,
                "Min values": min_values
            }

            outfile.write(json.dumps(out_record) + "\n")

    tqdm.write(f"Wrote {out_path}")