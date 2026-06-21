import numpy as np
import matplotlib.pyplot as plt
import json
from collections import Counter
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.legend_handler import HandlerBase
import seaborn as sns
import os
from pathlib import Path

CURRENT_WORKING_DIRECTORY = Path.cwd()

output_dir = f"{CURRENT_WORKING_DIRECTORY}/image_replication/fixed_grix_exp_results_images/"
os.makedirs(output_dir, exist_ok=True)

def make_image(map_type, num_r_units, map_number):
    """Creates five individual images, one for each block size, for a version of the fixed grid experiment where all other variables are fixed.

    Args:
    map_type: "high", "low", or "med", inidicating assoratativity variable.
    num_r_units: "72" or "86", indicatating partisanship variable.
    map_number: "1", "2", or "3", indicating choice of map variable.
    """
    colors_dict = {1:"#C777DB", 2: "#76C0D8", 3: "#FFC787", 4: "#8ED9B6", 6: "#FF8FA3"}

    one_data = np.load(f"{CURRENT_WORKING_DIRECTORY}/fixed_grid_experiment/processed_results_data/neutral_histogram_data/{map_type}_BR_score_r_units_{num_r_units}_map_{map_number}_block_size_1.jsonl_histogram.npy", allow_pickle=True)
    two_data = np.load(f"{CURRENT_WORKING_DIRECTORY}/fixed_grid_experiment/processed_results_data/neutral_histogram_data/{map_type}_BR_score_r_units_{num_r_units}_map_{map_number}_block_size_2.jsonl_histogram.npy", allow_pickle=True)
    three_data = np.load(f"{CURRENT_WORKING_DIRECTORY}/fixed_grid_experiment/processed_results_data/neutral_histogram_data/{map_type}_BR_score_r_units_{num_r_units}_map_{map_number}_block_size_3.jsonl_histogram.npy", allow_pickle=True)
    four_data = np.load(f"{CURRENT_WORKING_DIRECTORY}/fixed_grid_experiment/processed_results_data/neutral_histogram_data/{map_type}_BR_score_r_units_{num_r_units}_map_{map_number}_block_size_4.jsonl_histogram.npy", allow_pickle=True)
    six_data = np.load(f"{CURRENT_WORKING_DIRECTORY}/fixed_grid_experiment/processed_results_data/neutral_histogram_data/{map_type}_BR_score_r_units_{num_r_units}_map_{map_number}_block_size_6.jsonl_histogram.npy", allow_pickle=True)

    N = len(one_data)
    x = np.linspace(0, 12, N)

    rng = np.random.default_rng(seed=35)
    delta = 0.2
    delta_neg = -0.2

    def jitter_x(size):
        return rng.uniform(delta_neg, delta, size=size) * 0.5

    fig, ax = plt.subplots(figsize=(6, 4))

    # W]yte make an inidividual image for each block size
    for block_size in [1,2,3,4,6]:

        # Plot NN KDEs
        sns.kdeplot(
            x=np.linspace(0, 12, len(one_data)),
            weights=one_data,
            bw_adjust=0.8,
            color=colors_dict[1],
            ax=ax
        )
        sns.kdeplot(
            x=np.linspace(0, 12, len(two_data)),
            weights=two_data,
            bw_adjust=0.8,
            color=colors_dict[2],
            ax=ax
        )
        sns.kdeplot(
            x=np.linspace(0, 12, len(three_data)),
            weights=three_data,
            bw_adjust=0.8,
            color=colors_dict[3],
            ax=ax
        )
        sns.kdeplot(
            x=np.linspace(0, 12, len(four_data)),
            weights=four_data,
            bw_adjust=0.8,
            color=colors_dict[4],
            ax=ax
        )
        sns.kdeplot(
            x=np.linspace(0, 12, len(six_data)),
            weights=six_data,
            bw_adjust=0.8,
            color=colors_dict[6],
            ax=ax
        )

        # Plot vote share line
        if num_r_units == "72":
            ax.vlines(6,0, 1, color='black', linewidth=4)
        elif num_r_units == "86":
            ax.vlines(4.48, 0, 1, color='black', linewidth=4)

        # Plot NG maximums
        with open(f"{CURRENT_WORKING_DIRECTORY}/fixed_grid_experiment/processed_results_data/gerry_max_and_min_values/NG_maximums/{map_type}_BR_score_r_units_{num_r_units}_map_{map_number}.jsonl", 'r') as f:
            for line in f:
                data = json.loads(line)
                print(map_type + num_r_units + map_number)
                if data["block_size"] == f"block_size_{block_size}":
                    ax.vlines(
                        data["max_Seats_won_D_values"] + jitter_x(len(data["max_Seats_won_D_values"])),
                        0,
                        1,
                        linewidth=0.2,
                        alpha=0.2,
                        color=colors_dict[block_size]
                    )

            # Plot NG minimums
            with open(f"{CURRENT_WORKING_DIRECTORY}/fixed_grid_experiment/processed_results_data/gerry_max_and_min_values/NG_minimums/{map_type}_BR_score_r_units_{num_r_units}_map_{map_number}.jsonl", 'r') as fi:
                for line in fi:
                    data = json.loads(line)
                    if data["block_size"] == f"block_size_{block_size}":
                        ax.vlines(
                            data["min_Seats_won_D_values"] + jitter_x(len(data["min_Seats_won_D_values"])),
                            0,
                            1,
                            linewidth=0.2,
                            alpha=0.3,
                            color=colors_dict[block_size]
                        )

        ax.set_ylabel("")
        ax.set_xlim(-0.5, 12.5)
        plt.xticks(np.arange(0, 13, 1),fontsize=18)
        ax.tick_params(axis='x')
        ax.set_ylim(0, 1)
        ax.set_yticks([])
        to_save = Path(output_dir) / f"{map_type}_BR_score_r_units_{num_r_units}_map_{map_number}_block_size_{block_size}.png"
        os.makedirs(os.path.dirname(to_save), exist_ok=True)
        plt.tight_layout()
        fig.savefig(to_save,bbox_inches=None)
        ax.clear()


def main():
    """Creates all fixed grid experiment images.
    """
    for map_type in ["high", "low", "med"]:
        for num_r_units in ["72", "86"]:
            for map_number in ["1","2","3"]:
                make_image(map_type, num_r_units, map_number)

main()