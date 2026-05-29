import json
from pathlib import Path
import os

# Root folder
root = Path("/share/duchin/raina/REP_DATA/New_York_results/gerry/gerry_updaters")

# Output folder
output_file = "/share/duchin/raina/REPLICATION_REPO/NY_files/processed_results_data/gerry_max_and_min_values/gerry_toward_D_using_sen_data.jsonl"

# Iterate over geographic types
for geo_type in ["vtds", "blockgroups", "tracts"]:

    geo_path = root / geo_type
    for exp_folder in geo_path.iterdir():
        print(exp_folder)

        if not exp_folder.is_dir():
            print("skipping")
            continue
        exp_name = exp_folder.name
        if exp_name == "gerry_toward_D_using_pres_data":
            continue
        elif exp_name == "gerry_toward_R_using_pres_data":
            continue
        elif exp_name == "gerry_toward_R_using_sen_data":
            continue

        max_sen_values = []

        jsonl_files = sorted(exp_folder.glob("*.jsonl"))

        for i, f in enumerate(jsonl_files, start=1):
            max_sen_value = None

            with f.open() as infile:
                for line in infile:
                    plan = json.loads(line)
                    
                    sen_seats = plan.get("Sen seats won", {}).get("D", None)
                    if sen_seats is not None:
                        if max_sen_value is None or sen_seats > max_sen_value:
                            max_sen_value = sen_seats

            max_sen_values.append(max_sen_value)

            # Print progress
            print(f"  [{i}/{len(jsonl_files)}] {f.name} -> max_sen: {max_sen_value}")

        record = {
            "Block type": geo_type,
            "Max Vals": max_sen_values
        }

        with open(output_file, "a") as f:
            json.dump(record, f)
            f.write("\n")

        print(f"Saved {geo_type} -> {exp_name} sen maxes to {pres_file}")