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

# Neutral data
blockgroup_data = np.load("/share/duchin/raina/REPLICATION_REPO/MT_files/saved_hists_MT/blockgroups_pres_histogram.npy", allow_pickle=True)
tracts_data = np.load("/share/duchin/raina/REPLICATION_REPO/MT_files/saved_hists_MT/tracts_pres_histogram.npy", allow_pickle=True)
vtds_data = np.load("/share/duchin/raina/REPLICATION_REPO/MT_files/saved_hists_MT/vtds_pres_histogram.npy", allow_pickle=True)

plt.figure(figsize=(10, 4))

x = np.arange(0, 51, 1)  # 25 points
counts = np.array(vtds_data)
bin_width = 1
n = counts.sum()
vtds_density = counts / (n * bin_width)
plt.bar(x - 0.5, vtds_density, width=bin_width, align='edge', alpha=0.5, label="VTDs", color="gray")

sns.kdeplot(
    x=x,
    weights=vtds_data,
    bw_adjust=0.8,
    color = "gray"
)

# Plot vote share
plt.axvline(x=20.801, color='black', linewidth=4)
plt.axvline(x=25, color='black', linewidth=4,linestyle='--')

# Finish graph details
plt.xticks(np.arange(0, 51, 5), fontsize=18)
plt.yticks([])
plt.xlim(0, 50)
plt.ylim(0, 0.35)
plt.legend(handles=legend_elements,handler_map={BellCurveHandle: HandlerBellCurve()},loc='upper left', bbox_to_anchor=(1, 1))
plt.ylabel("")
plt.xlabel("Number of Democratic seats \n (50 possible)")
plt.ylabel("Count of plans")
plt.title("Comparing performance of different census units to neutral ensemble \n 2020 Presidential race, Montana")
plt.tight_layout()
plt.savefig("/share/duchin/raina/Montana_files/A_paper_images_compiled_2/gray_MT_pres_image_no_label.png",dpi=600)