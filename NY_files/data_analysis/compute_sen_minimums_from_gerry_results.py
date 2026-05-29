import json
from pathlib import Path
import os

# Root folder
root = Path("/share/duchin/raina/REP_DATA/New_York_results/gerry/gerry_updaters")

# Output folder
output_file = "/share/duchin/raina/REPLICATION_REPO/NY_files/processed_results_data/gerry_max_and_min_values/gerry_toward_R_using_sen_data.jsonl"

# Iterate over geographic types
for geo_type in ["vtds", "blockgroups", "tracts"]:

    geo_path = root / geo_type
    for exp_folder in geo_path.iterdir():

        if not exp_folder.is_dir():
            print("skipping")
            continue
        exp_name = exp_folder.name
        if exp_name == "gerry_toward_D_using_pres_data":
            continue
        elif exp_name == "gerry_toward_D_using_sen_data":
            continue
        elif exp_name == "gerry_toward_R_using_pres_data":
            continue

        min_sen_values = []

        jsonl_files = sorted(exp_folder.glob("*.jsonl"))

        for i, f in enumerate(jsonl_files, start=1):
            min_sen_value = None
            min_sen_value = None

            with f.open() as infile:
                for line in infile:
                    plan = json.loads(line)
                    
                    sen_seats = plan.get("Sen seats won", {}).get("D", None)
                    if sen_seats is not None:
                        if min_sen_value is None or sen_seats < min_sen_value:
                            min_sen_value = sen_seats

            min_sen_values.append(min_sen_value)

            # Print progress
            print(f"  [{i}/{len(jsonl_files)}] {f.name} -> min_sen: {min_sen_value}")

        record = {
            "Block type": geo_type,
            "Min Vals": min_sen_values
        }

        with open(output_file, "a") as f:
            json.dump(record, f)
            f.write("\n")

        print(f"Saved {geo_type} -> {exp_name} sen mins to {output_file}")