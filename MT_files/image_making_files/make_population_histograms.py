import numpy as np
from gerrychain import Graph
import matplotlib.pyplot as plt
import json
import os
import matplotlib.pyplot as plt
import seaborn as sns

CURRENT_WORKING_DIRECTORY = Path.cwd()

labels_dict = {"vtds": "Precincts", "blockgroups": "Block Groups", "tracts": "Tracts"}
colors_dict = {"vtds": "#76C0D8", "blockgroups": "#C777DB", "tracts": "#FFC787"}

for block_type in ["vtds", "blockgroups", "tracts"]:
    graph = Graph.from_json(f"{CURRENT_WORKING_DIRECTORY}/REPLICATION_REPO/MT_files/dual_graphs/{block_type}_dual_graph.json")

    pop = [d["total_pop"] for _, d in graph.nodes(data=True)]

    sns.set(style="whitegrid")

    bins = bins = np.linspace(0, 10000, 26)
    block_colors = ["#C777DB", "#76C0D8", "#FFC787"]

    plt.figure(figsize=(10, 6))
    sns.histplot(pop,
                color=colors_dict[block_type],
                label=labels_dict[block_type],
                kde=False,
                bins=bins)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)

    plt.ylim(0, 350)
    plt.xlim(0, 10000)
    plt.legend()
    plt.ylabel("")
    plt.tight_layout()

    save_location = f"{CURRENT_WORKING_DIRECTORY}/image_replication/MT_unit_population_images/{block_type}_populations.png"
    os.makedirs(save_location, exist_ok=True)
    plt.savefig(save_location, dpi=600)
