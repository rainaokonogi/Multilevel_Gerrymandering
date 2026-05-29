import json
from pathlib import Path
import os

# Root folder
root = Path("/share/duchin/raina/REP_DATA/New_York_results/gerry/gerry_updaters")

# Output folder
output_file = "/share/duchin/raina/REPLICATION_REPO/NY_files/processed_results_data/gerry_max_and_min_values/gerry_toward_D_using_pres_data.jsonl"

# Iterate over geographic types
for geo_type in ["vtds", "blockgroups", "tracts"]:

    geo_path = root / geo_type
    for exp_folder in geo_path.iterdir():
        print(exp_folder)

        if not exp_folder.is_dir():
            print("skipping")
            continue
        exp_name = exp_folder.name
        if exp_name == "gerry_toward_D_using_sen_data":
            continue
        elif exp_name == "gerry_toward_R_using_pres_data":
            continue
        elif exp_name == "gerry_toward_R_using_sen_data":
            continue

        max_pres_values = []

        jsonl_files = sorted(exp_folder.glob("*.jsonl"))

        for i, f in enumerate(jsonl_files, start=1):
            max_pres_value = None

            with f.open() as infile:
                for line in infile:
                    plan = json.loads(line)
                    
                    pres_seats = plan.get("Pres seats won", {}).get("D", None)
                    if pres_seats is not None:
                        if max_pres_value is None or pres_seats > max_pres_value:
                            max_pres_value = pres_seats

            max_pres_values.append(max_pres_value)

            # Print progress
            print(f"  [{i}/{len(jsonl_files)}] {f.name} -> max_pres: {max_pres_value}")

        record = {
            "Block type": geo_type,
            "Max Vals": max_pres_values
        }

        with output_file.open("a") as f:
            json.dump(record)

        print(f"Saved {geo_type} -> {exp_name} pres maxes to {output_file}")