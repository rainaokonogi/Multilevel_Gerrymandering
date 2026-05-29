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

CURRENT_WORKING_DIRECTORY = Path.cwd()

units_dict = {
    "vtds": {
        "label": "Precincts",
        "color": "#76C0D8"
    },
    "blockgroups": {
        "label": "Block Groups",
        "color": "#C777DB"
    },
    "tracts": {
        "label": "Tracts",
        "color": "#FFC787"
    }
}

make_plot_legend():
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

    straight_line_max = Line2D(
        [0], [0],
        color='black',
        linewidth=3,
        label='Maximum/minimum \n number of Dem seats \n from optimized searches'
    )

    straight_line_min = Line2D(
        [0], [0],
        color='black',
        linewidth=3,
        linestyle='--',
        label='Maximum/minimum \n number of Dem seats \n from neutral ensemble'
    )

    legend_elements = [
        Patch(facecolor=units_dict["vtds"][color], edgecolor=units_dict["vtds"][color], label='Precincts'),
        Patch(facecolor=units_dict["blockgroups"][color], edgecolor=units_dict["blockgroups"][color], label='Block Groups'),
        Patch(facecolor=units_dict["tracts"][color], edgecolor=units_dict["tracts"][color], label='Tracts'),
        Patch(facecolor="black", edgecolor="black", label='Dem vote share'),
        # Patch(facecolor='gray', edgecolor='gray', label='Distribution'),
        bell,
        straight_line_min,
        straight_line_max
    ]

    return legend_elements, handler_map

    
bins = np.arange(0, 51, 1)

blockgroup_data = np.load(f"{CURRENT_WORKING_DIRECTORY}/REPLICATION_REPO/MT_files/processed_results_data/neutral_histogram_data/blockgroups_pres_histogram.npy", allow_pickle=True)
tracts_data = np.load(f"{CURRENT_WORKING_DIRECTORY}/REPLICATION_REPO/MT_files/processed_results_data/neutral_histogram_data/tracts_pres_histogram.npy", allow_pickle=True)
vtds_data = np.load(f"{CURRENT_WORKING_DIRECTORY}/REPLICATION_REPO/MT_files/processed_results_data/neutral_histogram_data/vtds_pres_histogram.npy", allow_pickle=True)

plt.figure(figsize=(10, 4))

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
sns.kdeplot(
    x=bins,
    weights=vtds_data,
    bw_adjust=0.8,
    color=units_dict["vtds"]["color"]
)

rng = np.random.default_rng(seed=36)
delta = 0.5
delta_neg = -0.5

all_maxs = []
all_mins = []

with open(f"{CURRENT_WORKING_DIRECTORY}/REPLICATION_REPO/MT_results/processed_results_data/gerry_max_and_min_values/gerry_toward_D_using_pres_data.jsonl",'r') as f:
    for i, line in enumerate(f):
        data = json.loads(line)
        info = data["Max Vals"]
        counts = Counter(info)

        x_vals = np.array(sorted(counts.keys()))
        sizes = np.array([counts[x] for x in x_vals])

        expanded = np.repeat(x_vals, sizes)

        jitter = rng.uniform(delta_neg, delta, size=len(expanded)) * 0.5

        for xj in expanded + jitter:
            all_maxs.append((xj, i))

with open(f"{CURRENT_WORKING_DIRECTORY}/REPLICATION_REPO/MT_results/processed_results_data/gerry_max_and_min_values/gerry_toward_R_using_pres_data.jsonl",'r') as f:
    for i, line in enumerate(f):
        data = json.loads(line)
        info = data["Min Vals"]
        counts = Counter(info)

        x_vals = np.array(sorted(counts.keys()))
        sizes = np.array([counts[x] for x in x_vals])

        expanded = np.repeat(x_vals, sizes)

        jitter = rng.uniform(delta_neg, delta, size=len(expanded)) * 0.5

        for xj in expanded + jitter:
            all_mins.append((xj, i))

rng.shuffle(all_maxs)
rng.shuffle(all_mins)

for xj, i in all_maxs:
    plt.vlines(xj, 0, 0.35, linewidth=0.5, alpha=0.8, color=colors[i])

for xj, i in all_mins:
    plt.vlines(xj, 0, 0.35, linewidth=0.5, alpha=0.8, color=colors[i])

# Plot vote share
plt.axvline(x=20.801, color='black', linewidth=4)

legend_elements, handler_map = make_plot_legend()

plt.xticks(np.arange(0, 51, 5), fontsize=18)
plt.yticks([])
plt.xlim(0, 50)
plt.ylim(0, 0.35)
plt.legend(
    handles=legend_elements,
    handler_map=handler_map,
    loc='upper left',
    bbox_to_anchor=(1, 1)
)
plt.ylabel("")
plt.xlabel("Number of Democratic seats \n (50 possible)")
plt.ylabel("Count of plans")
plt.title("Comparing performance of different census units to neutral ensemble \n 2020 Presidential race, Montana")
plt.tight_layout()
plt.savefig(f"{CURRENT_WORKING_DIRECTORY}/REPLICATION_REPO/Montana_files/image_replication//final_results_images/MT_pres_results.png",dpi=600)



