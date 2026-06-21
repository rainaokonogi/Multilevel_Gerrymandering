
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

output_dir = f"{CURRENT_WORKING_DIRECTORY}/image_replication/6-12-24_grix_exp_results_images/"
os.makedirs(output_dir, exist_ok=True)

def make_image(grid_size, num_r_units):
    """Creates three individual images, one for each block size, for NxN-grid version of the experiment.

    Args:
    grid_size: 6, 12, or 24, indicating size of the grid.
    num_r_units: "18" or "21", indicatating partisanship variable (number of red units in the 6x6 grid).
    """
    colors_dict = {1:"#C777DB", 2: "#76C0D8", 3: "#FFC787"}

    one_data = np.load(f"{CURRENT_WORKING_DIRECTORY}/6-12-24_grid_experiment/processed_results_data/{grid_size}x{grid_size}_grid_results/NN/med_BR_r_units_{num_r_units}_map_1_block_size_1.jsonl_histogram.npy", allow_pickle=True)
    two_data = np.load(f"{CURRENT_WORKING_DIRECTORY}/6-12-24_grid_experiment/processed_results_data/{grid_size}x{grid_size}_grid_results/NN/med_BR_r_units_{num_r_units}_map_1_block_size_2.jsonl_histogram.npy", allow_pickle=True)
    three_data = np.load(f"{CURRENT_WORKING_DIRECTORY}/6-12-24_grid_experiment/processed_results_data/{grid_size}x{grid_size}_grid_results/NN/med_BR_r_units_{num_r_units}_map_1_block_size_3.jsonl_histogram.npy", allow_pickle=True)

    N = len(one_data)
    x = np.linspace(0, 6, N)

    rng = np.random.default_rng(seed=35)
    delta = 0.2
    delta_neg = -0.2

    def jitter_x(size):
        return rng.uniform(delta_neg, delta, size=size) * 0.5

    fig, ax = plt.subplots(figsize=(6, 4))

    # Make an inidividual image for each block size
    for block_size in [1,2,3]:

        # Plot NN KDEs
        if block_size == 1:
            sns.kdeplot(
                x=np.linspace(0, 6, len(one_data)),
                weights=one_data,
                bw_adjust=0.8,
                color=colors_dict[block_size],
                ax=ax
            )
        elif block_size == 2:
            sns.kdeplot(
                x=np.linspace(0, 6, len(two_data)),
                weights=two_data,
                bw_adjust=0.8,
                color=colors_dict[block_size],
                ax=ax
            )
        elif block_size == 3:
            sns.kdeplot(
                x=np.linspace(0, 6, len(three_data)),
                weights=three_data,
                bw_adjust=0.8,
                color=colors_dict[block_size],
                ax=ax
            )

        # Plot vote share line
        if num_r_units == "18":
            ax.vlines(3,0, 1, color='black', linewidth=3)
        elif num_r_units == "21":
            ax.vlines(2.5, 0, 1, color='black', linewidth=3)

        # Plot NG maximums
        with open(f"{CURRENT_WORKING_DIRECTORY}/6-12-24_grid_experiment/processed_results_data/{grid_size}x{grid_size}_grid_results/NG/NG_maximums/med_BR_r_units_{num_r_units}_map_1.jsonl", 'r') as f:
            for line in f:
                data = json.loads(line)
                if data["Block size"] == f"block_size_{block_size}":
                    ax.vlines(
                        data["Max values"] + jitter_x(len(data["Max values"])),
                        0,
                        1,
                        linewidth=0.2,
                        alpha=0.2,
                        color=colors_dict[block_size]
                    )

            # Plot NG minimums
            with open(f"{CURRENT_WORKING_DIRECTORY}/6-12-24_grid_experiment/processed_results_data/{grid_size}x{grid_size}_grid_results/NG/NG_minimums/med_BR_r_units_{num_r_units}_map_1.jsonl", 'r') as fi:
                for line in fi:
                    data = json.loads(line)
                    if data["Block size"] == f"block_size_{block_size}":
                        ax.vlines(
                            data["Min values"] + jitter_x(len(data["Min values"])),
                            0,
                            1,
                            linewidth=0.2,
                            alpha=0.3,
                            color=colors_dict[block_size]
                        )

        ax.set_ylabel("")
        ax.set_xlim(-0.5, 6.5)
        plt.xticks(np.arange(0, 7, 1),fontsize=18)
        ax.tick_params(axis='x')
        ax.set_ylim(0, 1)
        ax.set_yticks([])
        to_save = Path(output_dir) / f"{grid_size}x{grid_size}_results_images/med_BR_score_r_units_{num_r_units}_map_1_block_size_{block_size}.png"
        os.makedirs(os.path.dirname(to_save), exist_ok=True)
        plt.tight_layout()
        fig.savefig(to_save,bbox_inches=None)
        ax.clear()


def main():
    """Creates all 6-12-24 grid experiment images.
    """
    for grid_size in [6, 12, 24]:
        for num_r_units in ["18", "21"]:
            make_image(grid_size, num_r_units)

main()