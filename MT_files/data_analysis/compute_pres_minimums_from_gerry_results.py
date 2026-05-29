import json
from pathlib import Path
import os

# Root folder
root = "/share/duchin/raina/REPLICATION_REPO/MT_results/gerry_output_updaters"

# Output folder
output_root = "/share/duchin/raina/REPLICATION_REPO/MT_results/gerry_output_updaters/min_seats/gerry_R_POV"
os.makedirs(output_root, exist_ok=True)

# Iterate over geographic types
for geo_type in ["blockgroups", "tracts", "vtds"]:

    geo_path = Path(f"/share/duchin/raina/REPLICATION_REPO/MT_results/gerry_output_updaters/{geo_type}")
    for exp_folder in geo_path.iterdir():
        print(exp_folder)

        if not exp_folder.is_dir():
            print("skipping")
            continue
        exp_name = exp_folder.name
        if exp_name == "gerry_toward_D_using_pres_data":
            continue
        elif exp_name == "gerry_toward_D_using_sen_data":
            continue
        elif exp_name == "gerry_toward_R_using_sen_data":
            continue

        # Output folder
        pres_file = Path(f"/share/duchin/raina/REPLICATION_REPO/MT_results/gerry_output_updaters/min_seats/gerry_R_POV/{geo_type}_{exp_name}_pres.jsonl")

        min_pres_values = []
        min_sen_values = []

        # Collect all .jsonl files and sort
        jsonl_files = sorted(exp_folder.glob("*.jsonl"))

        for i, f in enumerate(jsonl_files, start=1):
            min_pres_value = None
            min_sen_value = None

            with f.open() as infile:
                for line in infile:
                    plan = json.loads(line)
                    
                    pres_seats = plan.get("Pres seats won", {}).get("D", None)
                    if pres_seats is not None:
                        if min_pres_value is None or pres_seats < min_pres_value:
                            min_pres_value = pres_seats

            min_pres_values.append(min_pres_value)

            # Print progress
            print(f"  [{i}/{len(jsonl_files)}] {f.name} -> max_pres: {min_pres_value}")

        record = {
            "Block type": geo_type,
            "Min Vals": min_pres_values
        }

        with pres_file.open("a") as f:
            json.dump(record)

        print(f"Saved {geo_type} -> {exp_name} pres maxes to {pres_file}")