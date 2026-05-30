import json
from pathlib import Path
import os

CURRENT_WORKING_DIRECTORY = Path.cwd()

def main():
    """Performs data analysis on some of the Montana experiment results.
    Specifically, looks at the short bursts optimization runs gerrymandered toward Democrats using Sen2022 data
    and saves the maximum number of seats won by Democrats in any plan for each chain.
    """
    # Root folder
    root = Path(f"{CURRENT_WORKING_DIRECTORY}/REP_DATA/Montana_results/gerry/gerry_updaters")

    if not root.exists():
        raise FileNotFoundError(
            f"Montana gerrymandered results folder not found.\n"
            "This data is available from the author upon request.\n"
        )

    # Output folder
    output_file = f"{CURRENT_WORKING_DIRECTORY}/MT_files/processed_results_data_(replicated)/gerry_max_and_min_values/gerry_toward_D_using_sen_data.jsonl"
    os.makedirs(output_file, exist_ok=True)

    # Find maximums for all three types of census units
    for geo_type in ["vtds", "blockgroups", "tracts"]:

        geo_path = root / geo_type
        for exp_folder in geo_path.iterdir():

            # Access data from experiment gerrymandering toward Democrats using Sen2022 data
            if not exp_folder.is_dir():
                print("skipping; not a directory")
                continue
            exp_name = exp_folder.name
            if exp_name != "gerry_toward_D_using_sen_data":
                continue

            max_sen_values = []

            jsonl_files = sorted(exp_folder.glob("*.jsonl"))

            for i, f in enumerate(jsonl_files, start=1):
                max_sen_value = None

                with f.open() as infile:
                    for line in infile:
                        plan = json.loads(line)
                        
                        # For each step in chain, check if the number of seats won by Dems is the new maximum
                        sen_seats = plan.get("Sen seats won", {}).get("D", None)
                        if sen_seats is not None:
                            if max_sen_value is None or sen_seats > max_sen_value:
                                max_sen_value = sen_seats

                # Save the max val for each individual chain
                max_sen_values.append(max_sen_value)

                # Print progress
                print(f"  [{i}/{len(jsonl_files)}] {f.name} -> max_sen: {max_sen_value}")

            # Save results
            record = {
                "Block type": geo_type,
                "Max Vals": max_sen_values
            }

            with open(output_file, "a") as f:
                json.dump(record, f)
                f.write("\n")

main()