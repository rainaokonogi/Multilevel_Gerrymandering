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

colors = ["#C777DB", "#76C0D8", "#FFC787"]

# Neutral data
blockgroup_data = np.load("/share/duchin/raina/REPLICATION_REPO/MT_files/saved_hists_MT/blockgroups_sen_histogram.npy", allow_pickle=True)
vtds_data = np.load("/share/duchin/raina/REPLICATION_REPO/MT_files/saved_hists_MT/vtds_sen_histogram.npy", allow_pickle=True)
tracts_data = np.load("/share/duchin/raina/REPLICATION_REPO/MT_files/saved_hists_MT/tracts_sen_histogram.npy", allow_pickle=True)

plt.figure(figsize=(10, 4))

# print(blockgroup_data)
# print(vtds_data)
# print(tracts_data)

# Data for neutral min/maxes
# nonzero_indices_blockgroups = np.nonzero(blockgroup_data)[0]
# nonzero_indices_tracts = np.nonzero(tracts_data)[0]
# nonzero_indices_vtds = np.nonzero(vtds_data)[0]

# xmin_blockgroups = nonzero_indices_blockgroups.min()
# xmin_tracts = nonzero_indices_tracts.min()
# xmin_vtds = nonzero_indices_vtds.min()

# xmax_blockgroups = nonzero_indices_blockgroups.max()
# xmax_tracts = nonzero_indices_tracts.max()
# xmax_vtds = nonzero_indices_vtds.max()

x = np.arange(0, 51, 1)  # 25 points
counts = np.array(vtds_data)
bin_width = 1
n = counts.sum()
vtds_density = counts / (n * bin_width)
# plt.bar(x - 0.5, vtds_density, width=bin_width, align='edge', alpha=0.5, label="VTDs", color="gray")

# x = range(0,len(vtds_data))
# colors = ["#7F58AF", "#64C5EB", "#E84D8A"]

# Plot histograms
# plt.bar(x, blockgroup_data, alpha=0.5, label="Block Groups", color=colors[0])
# plt.bar(x, tracts_data, alpha=0.5, label="Tracts", color=colors[1])
# plt.bar(x, vtds_data, alpha=0.5, label="Precincts", color=colors[2])

sns.kdeplot(
    x=x,
    weights=blockgroup_data,
    bw_adjust=0.8,
    color=colors[0]
)
sns.kdeplot(
    x=x,
    weights=tracts_data,
    bw_adjust=0.8,
    color=colors[1]
)
sns.kdeplot(
    x=x,
    weights=vtds_data,
    bw_adjust=0.8,
    color =colors[2]
    # color=colors[2]
)


# Plot curves over histograms
# plt.plot(x, blockgroup_data, linewidth=2, color=colors[0])
# plt.plot(x, tracts_data, linewidth=2, color=colors[1])
# plt.plot(x, vtds_data, linewidth=2, color=colors[2])

# Prep for random jitter
rng = np.random.default_rng(seed=36)
delta = 0.5
delta_neg = -0.5

all_points = []

with open("/share/duchin/raina/REPLICATION_REPO/MT_results/gerry_max_and_min_values/gerry_D_POV/A_gerry_toward_D_using_sen_data_sen.jsonl",'r') as f:
    for i, line in enumerate(f):
        data = json.loads(line)
        info = data["Max Vals"]
        counts = Counter(info)

        x_vals = np.array(sorted(counts.keys()))
        sizes = np.array([counts[x] for x in x_vals])

        expanded = np.repeat(x_vals, sizes)

        jitter = rng.uniform(delta_neg, delta, size=len(expanded)) * 0.5

        # store everything instead of plotting immediately
        for xj in expanded + jitter:
            all_points.append((xj, i))   # i = color index

rng.shuffle(all_points)

for xj, i in all_points:
    plt.vlines(xj, 0, 0.35, linewidth=0.5, alpha=0.8, color=colors[i])

all_points = []

with open("/share/duchin/raina/REPLICATION_REPO/MT_results/gerry_max_and_min_values/gerry_R_POV/A_gerry_toward_R_using_sen_data_sen.jsonl",'r') as f:
    for i, line in enumerate(f):
        data = json.loads(line)
        info = data["Min Vals"]
        # transformed_info = [63 - x for x in info]
        counts = Counter(info)

        x_vals = np.array(sorted(counts.keys()))
        sizes = np.array([counts[x] for x in x_vals])

        expanded = np.repeat(x_vals, sizes)

        jitter = rng.uniform(delta_neg, delta, size=len(expanded)) * 0.5

        # store everything instead of plotting immediately
        for xj in expanded + jitter:
            all_points.append((xj, i))   # i = color index

rng.shuffle(all_points)

for xj, i in all_points:
    plt.vlines(xj, 0, 0.35, linewidth=0.5, alpha=0.8, color=colors[i])


# Plot vote share
plt.axvline(x=22.494, color='black', linewidth=4)



# Plot neutral mins/maxes
# plt.axvline(xmin_blockgroups + rng.uniform(delta_neg, delta), color=colors[0], linewidth=1.5, linestyle='--')
# plt.axvline(xmax_blockgroups + rng.uniform(delta_neg, delta), color=colors[0], linewidth=1.5, linestyle='--')
# plt.axvline(xmin_tracts + rng.uniform(delta_neg, delta), color=colors[1], linewidth=1.5, linestyle='--')
# plt.axvline(xmax_tracts + rng.uniform(delta_neg, delta), color=colors[1], linewidth=1.5, linestyle='--')
# plt.axvline(xmin_vtds + rng.uniform(delta_neg, delta), color=colors[2],linewidth=1.5, linestyle='--')
# plt.axvline(xmax_vtds + rng.uniform(delta_neg, delta), color=colors[2], linewidth=1.5, linestyle='--')

# Make legend
x = np.linspace(0, 1, 50)
y = np.exp(-((x - 0.5) ** 2) / 0.02)  # bell-shaped "curve"

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
    Patch(facecolor=colors[2], edgecolor=colors[2], label='Precincts'),
    Patch(facecolor=colors[0], edgecolor=colors[0], label='Block Groups'),
    Patch(facecolor=colors[1], edgecolor=colors[1], label='Tracts'),
    Patch(facecolor="black", edgecolor="black", label='Dem vote share'),
    # Patch(facecolor='gray', edgecolor='gray', label='Distribution'),
    bell,
    straight_line_min,
    straight_line_max
]

# Finish graph details
plt.xticks(np.arange(0, 51, 5), fontsize=18)
plt.yticks([])
plt.xlim(0, 50)
plt.ylim(0, 0.35)
# plt.legend(handles=legend_elements,handler_map={BellCurveHandle: HandlerBellCurve()},loc='upper left', bbox_to_anchor=(1, 1))
plt.ylabel("")
# plt.xlabel("Number of Democratic seats \n (50 possible)")
# plt.ylabel("Count of plans")
# plt.title("Comparing performance of different census units to neutral ensemble \n 2020 Presidential race, Montana")
plt.tight_layout()
plt.savefig("/share/duchin/raina/Montana_files/A_paper_images_compiled_2/MT_TEST_SEN_IMAGE.png",dpi=600)