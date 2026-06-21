import numpy as np
import matplotlib.pyplot as plt
import json
from collections import Counter
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.legend_handler import HandlerBase
from scipy.stats import gaussian_kde
import random
import seaborn as sns
from pathlib import Path
import os

CURRENT_WORKING_DIRECTORY = Path.cwd()

output_dir = f"{CURRENT_WORKING_DIRECTORY}/image_replication/final_results_images/"
os.makedirs(output_dir, exist_ok=True)

units_dict = {
    "vtds": {
        "label": "Precincts",
        "color": "#FFC787"
    },
    "blockgroups": {
        "label": "Block Groups",
        "color": "#C777DB"
    },
    "tracts": {
        "label": "Tracts",
        "color": "#76C0D8"
    }
}

def make_plot_legend():
    x = np.linspace(0, 1, 50)
    y = np.exp(-((x - 0.5) ** 2) / 0.02)

    class BellCurveHandle:
        def __init__(self, color='black', label='Distribution of \n number of \n Democratic seats \n across neutral searches'):
            self.color = color
            self._label = label

        def get_label(self):
            return self._label

    class HandlerBellCurve(HandlerBase):
        def create_artists(self, legend, orig_handle,
                        xdescent, ydescent, width, height,
                        fontsize, trans):

            x = np.linspace(0, width, 50)

            y = height * np.exp(-((x - width/2) ** 2) / (2 * (width/6)**2))

            line = Line2D(
                x - xdescent,
                y - ydescent,
                color=orig_handle.color,
                linewidth=2
            )
            line.set_transform(trans)
            return [line]

    bell = BellCurveHandle(color='black')

    handler_map = {
        BellCurveHandle: HandlerBellCurve()
    }

    legend_elements = [
        Patch(facecolor=units_dict["vtds"]["color"], edgecolor=units_dict["vtds"]["color"], label='Precincts'),
        Patch(facecolor=units_dict["blockgroups"]["color"], edgecolor=units_dict["blockgroups"]["color"], label='Block Groups'),
        Patch(facecolor=units_dict["tracts"]["color"], edgecolor=units_dict["tracts"]["color"], label='Tracts'),
        Patch(facecolor="black", edgecolor="black", label='Dem vote share'),
        bell
    ]

    return legend_elements, handler_map

def main():
    """Creates one image summarizing the results of the MT experiments using Pres2020 data.
    Image will include KDEs for the number of Democratic seats across neutral runs,
    the maximum number of Democratic seats found for runs gerrymandered toward Dems,
    and the minumum number of Democratic seats found for runs gerrymandered toward Reps.
    """
    bins = np.arange(0, 51, 1)

    vtds_data = np.load(f"{CURRENT_WORKING_DIRECTORY}/MT_files/processed_results_data/neutral_histogram_data/vtds_pres_histogram.npy", allow_pickle=True)
    blockgroup_data = np.load(f"{CURRENT_WORKING_DIRECTORY}/MT_files/processed_results_data/neutral_histogram_data/blockgroups_pres_histogram.npy", allow_pickle=True)
    tracts_data = np.load(f"{CURRENT_WORKING_DIRECTORY}/MT_files/processed_results_data/neutral_histogram_data/tracts_pres_histogram.npy", allow_pickle=True)

    plt.figure(figsize=(10, 4))

    sns.kdeplot(
        x=bins,
        weights=vtds_data,
        bw_adjust=0.8,
        color=units_dict["vtds"]["color"]
    )
    sns.kdeplot(
        x=bins,
        weights=blockgroup_data,
        bw_adjust=0.8,
        color=units_dict["blockgroups"]["color"]
    )
    sns.kdeplot(
        x=bins,
        weights=tracts_data,
        bw_adjust=0.8,
        color=units_dict["tracts"]["color"]
    )

    rng = np.random.default_rng(seed=36)
    delta = 0.5
    delta_neg = -0.5

    all_maxs = []
    all_mins = []

    with open(f"{CURRENT_WORKING_DIRECTORY}/MT_files/processed_results_data/gerry_max_and_min_values/gerry_toward_D_using_pres_data.jsonl",'r') as f:
        for i, line in enumerate(f):
            data = json.loads(line)
            block_type = data["Block type"]
            info = data["Max Vals"]
            counts = Counter(info)

            x_vals = np.array(sorted(counts.keys()))
            sizes = np.array([counts[x] for x in x_vals])

            expanded = np.repeat(x_vals, sizes)

            jitter = rng.uniform(delta_neg, delta, size=len(expanded)) * 0.5

            for xj in expanded + jitter:
                all_maxs.append((xj, block_type))

    with open(f"{CURRENT_WORKING_DIRECTORY}/MT_files/processed_results_data/gerry_max_and_min_values/gerry_toward_R_using_pres_data.jsonl",'r') as f:
        for i, line in enumerate(f):
            data = json.loads(line)
            block_type = data["Block type"]
            info = data["Min Vals"]
            counts = Counter(info)

            x_vals = np.array(sorted(counts.keys()))
            sizes = np.array([counts[x] for x in x_vals])

            expanded = np.repeat(x_vals, sizes)

            jitter = rng.uniform(delta_neg, delta, size=len(expanded)) * 0.5

            for xj in expanded + jitter:
                all_mins.append((xj, block_type))

    rng.shuffle(all_maxs)
    rng.shuffle(all_mins)

    for xj, block_type in all_maxs:
        plt.vlines(xj, 0, 0.35, linewidth=0.5, alpha=0.8, color=units_dict[block_type]["color"])

    for xj, block_type in all_mins:
        plt.vlines(xj, 0, 0.35, linewidth=0.5, alpha=0.8, color=units_dict[block_type]["color"])

    # Plot vote share
    plt.axvline(x=20.801, color='black', linewidth=4)

    legend_elements, handler_map = make_plot_legend()

    plt.xticks(np.arange(0, 51, 5), fontsize=18)
    plt.yticks([])
    plt.xlim(-1,51)
    plt.ylim(0, 0.35)
    plt.ylabel("")
    # plt.legend(
    #     handles=legend_elements,
    #     handler_map=handler_map,
    #     loc='upper left',
    #     bbox_to_anchor=(1, 1)
    # )
    # plt.xlabel("Number of Democratic seats \n (63 possible)")
    # plt.ylabel("Count of plans")
    # plt.title("Comparing performance of different census units to neutral ensemble \n 2020 Presidential race, Montana")
    plt.tight_layout()
    plt.savefig(Path(output_dir) / "MT_pres_results.png", dpi=600)

main()