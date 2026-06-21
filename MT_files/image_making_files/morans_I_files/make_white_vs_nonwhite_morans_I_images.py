import json
import numpy as np
import matplotlib.pyplot as plt
from libpysal.weights import W
from esda.moran import Moran
import scipy.sparse as sp
from pathlib import Path

CURRENT_WORKING_DIRECTORY = Path.cwd()

def make_image(block_type):
    """
    For a census unit in Motana, compute the Moran's I score of Democrats and Republicans (determined using some voter data).
    Create a scatter plot where each x-value plots the percentage of Democrats in each unit and each y-value is the average 
    percentage of Democrats in neighboring units.

    Args:
    block_type (str): The census unit we're computing Moran's I/making image for ("vtds", "blockgroups", "tracts", or "counties).
    """

    file_to_open = f"{CURRENT_WORKING_DIRECTORY}/MT_files/dual_graphs/morans_i_graphs/white_v_nonwhite/MT_{block_type}_dual_graph_{election}_for_moran.json"
    with open(file_to_open) as f:
        data = json.load(f)

        node_id_to_index_dict = {
            node["id"]: i
            for i, node in enumerate(data["nodes"])
        }

        x_values_index_to_vote_percentage = {}

        for i, node in enumerate(data["nodes"]):
            if if node["total_pop"] != 0:
                x_values_index_to_vote_percentage[i] = node["white_pop"] / node["total_pop"]
            else:
                raise ValueError( # We should have gotten rid of these nodes in pre-processing
                f"Found node with zero total population."
            )

        n = len(x_values_index_to_vote_percentage)

        x = np.array([
            x_values_index_to_vote_percentage[i]
            for i in range(n)
        ])

        adjacency = data["adjacency"]

        adjacency_dict = {
            i: [node_id_to_index_dict[neighbor["id"]] for neighbor in adjacency[i]]
            for i in range(n)
        }

        y_lag = np.array([
            np.mean([x[j] for j in adjacency_dict[i]]) if adjacency_dict[i] else 0
            for i in range(n)
        ])

        # Compute Moran's I value
        w = W(adjacency_dict)
        w.transform = "R"
        moran = Moran(x, w)

        # Plot scatter plot
        plt.scatter(x, y_lag, color='CornflowerBlue', alpha=0.6)

        # Plot line of best fit
        m, b = np.polyfit(x, y_lag, 1)
        plt.plot(x, m*x + b, color="salmon")

        # We print these values to confirm the Moran's I score matches the slope of the line of best fit
        print(moran.I)
        print(m)

        plt.xlim(0, 1)
        plt.ylim(0, 1)

        plt.xticks(np.linspace(0, 1, 6), fontsize=18)  # 0, 0.2, ..., 1
        plt.yticks(np.linspace(0, 1, 6), fontsize=18)

        plt.gca().set_aspect('equal', adjustable='box')
        plt.title(f"I = {moran.I:.3f}", fontsize=18)
        plt.tight_layout()
        save_location = f"{CURRENT_WORKING_DIRECTORY}/image_replication/MT_morans_i_images//MT_white_v_nonwhite_{election}_{block_type}_morans_i.png"
        os.makedirs(os.path.dirname(save_location), exist_ok=True)
        plt.savefig(save_location)
        plt.close()


def main():
    """
    Make images for all four census units using both sets of voter data.
    """
    for block_type in ["vtds", "blockgroups", "tracts", "counties"]:
        make_image(block_type)

main()