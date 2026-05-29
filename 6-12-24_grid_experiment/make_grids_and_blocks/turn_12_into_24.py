import json
import networkx as nx
import os
from gerrychain import Graph
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.colors import ListedColormap, BoundaryNorm
import numpy as np

input_file = "/share/duchin/raina/6-12-24_grid_exp/12x12_unit_maps/map_.jsons/med_BR_r_units_18_map_1.json"
output_file = "/share/duchin/raina/6-12-24_grid_exp/24x24_unit_maps/map_.jsons/med_BR_r_units_18_map_1.json"

# -------------------------------------------------
# Load raw JSON
# -------------------------------------------------

with open(input_file) as f:
    data = json.load(f)

nodes = data["nodes"]

# -----------------------------
# Build lookup: (row, col) -> attrs
# -----------------------------
lookup = {}
for n in nodes:
    row, col = n["old_node_index"]
    lookup[(row, col)] = n

# -----------------------------
# Build new nodes (12x12)
# -----------------------------
new_nodes = []
coord_to_id = {}

new_id = 0

for r in range(12):
    for c in range(12):

        attrs = lookup[(r, c)]

        for dr in [0, 1]:
            for dc in [0, 1]:

                nr = 2 * r + dr
                nc = 2 * c + dc

                coord_to_id[(nr, nc)] = new_id

                new_nodes.append({
                    "old_node_index": [nr, nc],
                    "population": 1,
                    "D": attrs["D"],
                    "R": attrs["R"],
                    "id": new_id
                })

                new_id += 1

# -----------------------------
# Build adjacency (12x12 grid)
# -----------------------------
adjacency = []

for r in range(24):
    for c in range(24):

        nid = coord_to_id[(r, c)]
        nbrs = []

        if r > 0:
            nbrs.append({"id": coord_to_id[(r - 1, c)]})
        if r < 23:
            nbrs.append({"id": coord_to_id[(r + 1, c)]})
        if c > 0:
            nbrs.append({"id": coord_to_id[(r, c - 1)]})
        if c < 23:
            nbrs.append({"id": coord_to_id[(r, c + 1)]})

        adjacency.append(nbrs)

# -----------------------------
# Output JSON (same structure)
# -----------------------------
out = {
    "directed": False,
    "multigraph": False,
    "graph": [],
    "nodes": new_nodes,
    "adjacency": adjacency
}

with open(output_file, "w") as f:
    json.dump(out, f)

print("Wrote:", output_file)

def create_dual_graph_image(num_r_units, map_number):

    save_grid_map_images_to = (
        f"/share/duchin/raina/6-12-24_grid_exp/24x24_unit_maps/"
        f"map_.pngs/med_BR_r_units_{num_r_units}_map_{map_number}.png"
    )

    os.makedirs(os.path.dirname(save_grid_map_images_to), exist_ok=True)

    unit_dual_graph_json = (
        f"/share/duchin/raina/6-12-24_grid_exp/24x24_unit_maps/"
        f"map_.jsons/med_BR_r_units_{num_r_units}_map_{map_number}.json"
    )

    unit_dual_graph = Graph.from_json(unit_dual_graph_json)

    # -------------------------------------------------
    # Build empty 12x12 grid
    # -------------------------------------------------
    grid = np.zeros((24, 24), dtype=int)

    for _, data in unit_dual_graph.nodes(data=True):

        row, col = data["old_node_index"]

        # IMPORTANT: row = y, col = x
        grid[row][col] = int(data["D"])

    # -------------------------------------------------
    # Plot
    # -------------------------------------------------
    cmap = matplotlib.colors.ListedColormap(['#E62020', '#1560BD'])
    bounds = [0, 1]
    norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)

    fig, ax = plt.subplots()
    ax.imshow(grid, cmap=cmap, norm=norm)

    ax.set_xticks(np.arange(-0.5, 24, 1))
    ax.set_yticks(np.arange(-0.5, 24, 1))
    ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)

    ax.set_xticklabels([])
    ax.set_yticklabels([])

    plt.savefig(save_grid_map_images_to)

create_dual_graph_image(18, 1)
