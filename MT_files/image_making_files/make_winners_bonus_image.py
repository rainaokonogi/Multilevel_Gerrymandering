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

def main():

    # Neutral data
    vtds_data = np.load(f"{CURRENT_WORKING_DIRECTORY}/MT_files/processed_results_data/neutral_histogram_data/vtds_pres_histogram.npy", allow_pickle=True)
    blockgroup_data = np.load(f"{CURRENT_WORKING_DIRECTORY}/MT_files/processed_results_data/neutral_histogram_data/blockgroups_pres_histogram.npy", allow_pickle=True)
    tracts_data = np.load(f"{CURRENT_WORKING_DIRECTORY}/MT_files/processed_results_data/neutral_histogram_data/tracts_pres_histogram.npy", allow_pickle=True)

    plt.figure(figsize=(10, 4))

    x = np.arange(0, 51, 1)  # 25 points
    counts = np.array(vtds_data)
    bin_width = 1
    n = counts.sum()
    vtds_density = counts / (n * bin_width)
    plt.bar(x - 0.5, vtds_density, width=bin_width, align='edge', alpha=0.5, label="Precincts", color="gray")

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
    plt.ylabel("")
    # plt.xlabel("Number of Democratic seats \n (50 possible)")
    # plt.ylabel("Count of plans")
    # plt.title("Comparing performance of different census units to neutral ensemble \n 2020 Presidential race, Montana")
    plt.tight_layout()
    plt.savefig(Path(output_dir) / "winners_bonus_image.png", dpi=600)

main()