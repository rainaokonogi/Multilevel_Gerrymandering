from pathlib import Path
from pyben import PyBenDecoder, PyBenEncoder
from gerrychain import Graph, Partition
import json
import pandas as pd
from gerrychain.updaters import cut_edges
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

CURRENT_WORKING_DIRECTORY = Path.cwd()

def collect_data(census_unit, party, election):

    save_file = f"{CURRENT_WORKING_DIRECTORY}/image_replication/MT_search_images/MT_search_{census_unit}_{election}_{party}.jsonl"

    updaters_folder = Path(f"{CURRENT_WORKING_DIRECTORY}/REPLICATION_REPO/MT_results/gerry_output_updaters/{census_unit}/gerry_toward_{party}_using_{election}_data")

    for i, file_path in enumerate(updaters_folder.glob("*.jsonl")):

        list_of_seats_won = []

        with open(file_path, 'r') as f:
            for j, line in enumerate(f):
                line = json.loads(line)
                if election == "pres":
                    num_seats = line["Pres seats won"][party]
                elif election == "sen":
                    num_seats = line["Sen seats won"][party]
                if j % 20 == 0:
                    if party == "R":
                        list_of_seats_won.append(50 - num_seats)
                    elif party == "D":
                        list_of_seats_won.append(num_seats)

        record = {
            "Census units": census_unit,
            "Party": party,
            "File": str(file_path),
            "Seats": list_of_seats_won
        }

        with open(save_file, "a") as f:
            f.write(json.dumps(record) + "\n")

def make_image():

    census_config = {
        "vtds": {
            "color": "#FFC787",
            "label": "Precincts"
        },
        "blockgroups": {
            "color": "#C777DB",
            "label": "Block Groups"
        },
        "tracts": {
            "color": "#76C0D8",
            "label": "Tracts"
        }
    }

    plt.figure(figsize=(8,6))

    for party in ["D", "R"]:
        for census_units, config in census_config.items():

            color = config["color"]

            data = f"{CURRENT_WORKING_DIRECTORY}/REPLICATION_REPO/MT_results/image_data/MT_search_{census_units}_{party}_pres.jsonl"

            with open(data, "r") as f:
                for i, line in enumerate(f):
                    line_obj = json.loads(line)
                    seats_list = line_obj["Seats"]

                    if party == "R":
                        seats_list = [50 - s for s in seats_list]

                    try:
                        last_change_idx = max(
                            i for i in range(1, len(seats_list))
                            if seats_list[i] != seats_list[i - 1]
                        )
                    except ValueError:
                        continue

                    seats_list = seats_list[:last_change_idx + 1]
                    steps_list = [i * 20 for i in range(len(seats_list))]

                    plt.plot(steps_list, seats_list, linewidth=1, color=color)
                    plt.scatter(steps_list[-1], seats_list[-1], color=color, s=20, zorder=3)

    # Legend built from same mapping (guaranteed consistent)
    handles = [
        Patch(facecolor=config["color"], edgecolor='none', label=config["label"])
        for config in census_config.values()
    ]

    # plt.legend(handles=handles, loc="upper right", bbox_to_anchor=(1, 0.55), fontsize=12)
    plt.ylim(0,30)
    plt.yticks(fontsize=16)
    plt.xticks(fontsize=16)
    plt.tight_layout()

    plt.savefig(
        f"{CURRENT_WORKING_DIRECTORY}/image_replication/MT_search_images/MT_pres_search.png",
        bbox_inches="tight",
        dpi=600
    )

def main():
    for party in ["D","R"]:
        for election in ["pres","sen"]:
            for census_unit in ["vtds","blockgroups","tracts"]:
                collect_data(census_unit, party, election)

make_image()