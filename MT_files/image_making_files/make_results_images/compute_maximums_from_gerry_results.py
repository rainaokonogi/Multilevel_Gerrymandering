import json
from pathlib import Path
import os

# Root folder
root = Path("MT_outputs_3/output_updaters_gerry")

# Output folder
output_root = root / "min_seats" / "gerry_R_POV"
os.makedirs(output_root, exist_ok=True)

# Iterate over geographic types
for geo_type in ["blockgroups", "tracts", "vtds"]:

    geo_path = root / geo_type
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
        pres_file = output_root / f"{geo_type}_{exp_name}_sen.jsonl"

        min_pres_values = []
        min_sen_values = []

        # Collect all .jsonl files and sort
        jsonl_files = sorted(exp_folder.glob("*.jsonl"))

        # print(f"\nProcessing {geo_type} -> {exp_name} ({len(jsonl_files)} files)")
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

                    # sen_seats = plan.get("Sen seats won", {}).get("D", None)
                    # if sen_seats is not None:
                    #     if max_sen_value is None or sen_seats > max_sen_value:
                    #         max_sen_value = sen_seats

            min_pres_values.append(min_pres_value)
            # max_sen_values.append(max_sen_value)

            # Print progress
            print(f"  [{i}/{len(jsonl_files)}] {f.name} -> max_pres: {min_pres_value}")

        # Save individual files

        # sen_file = output_root / f"{geo_type}_{exp_name}_sen.json"

        with pres_file.open("w") as f:
            json.dump(min_pres_values, f, indent=2)
        # with sen_file.open("w") as f:
        #     json.dump(max_sen_values, f, indent=2)

        print(f"Saved {geo_type} -> {exp_name} pres maxes to {pres_file}")
 #       print(f"Saved {geo_type} -> {exp_name} sen maxes to {sen_file}")