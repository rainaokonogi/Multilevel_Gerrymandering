import os
import json
import csv

BASE_DIR = "/share/duchin/raina/6-12-24_grid_exp/12_results_updaters/NN"
OUT_DIR = "/share/duchin/raina/6-12-24_grid_exp/12_results_updaters/NN_compiled"

os.makedirs(OUT_DIR, exist_ok=True)

for run_folder in os.listdir(BASE_DIR):
    run_path = os.path.join(BASE_DIR, run_folder)
    if not os.path.isdir(run_path):
        continue

    for block_folder in os.listdir(run_path):
        block_path = os.path.join(run_path, block_folder)
        if not os.path.isdir(block_path):
            continue

        out_name = f"{run_folder}__{block_folder}.jsonl"
        out_path = os.path.join(OUT_DIR, out_name)

        with open(out_path, "w") as outfile:

            # iterate over samples
            for sample_folder in sorted(os.listdir(block_path)):
                sample_path = os.path.join(block_path, sample_folder)
                if not os.path.isdir(sample_path):
                    continue

                seats_list = []

                # read all jsonl files in this sample
                for fname in os.listdir(sample_path):
                    if not (
                        fname.startswith("init_part_")
                        and "steps_20000" in fname
                        and fname.endswith("_updaters.jsonl")
                    ):
                        continue

                    fpath = os.path.join(sample_path, fname)

                    with open(fpath) as f:
                        for line in f:
                            if not line.strip():
                                continue
                            try:
                                record = json.loads(line)
                                seats_d = record["Seats won"]["D"]
                                seats_without_ties = record["Seats won"]["D"] + record["Seats won"]["R"]
                                if seats_without_ties != 6:
                                    seats_d = seats_d + 0.5*(6 - seats_without_ties)
                                seats_list.append(seats_d)
                            except (KeyError, json.JSONDecodeError):
                                continue

                # write ONE line per sample containing the full list
                out_record = {
                    "sample": sample_folder,
                    "Seats_won_D": seats_list
                }

                outfile.write(json.dumps(out_record) + "\n")

                print(
                    f"{run_folder}/{block_folder}/{sample_folder}: "
                    f"{len(seats_list)} values"
                )

        print(f"Wrote {out_path}")