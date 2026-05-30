import networkx as nx
import numpy as np
import random
import os
from gerrychain import Graph
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.colors import ListedColormap, BoundaryNorm
from scipy.ndimage import gaussian_filter

SCRIPT_FILE_PATH = os.path.abspath(__file__)
SCRIPT_DIR = os.path.dirname(SCRIPT_FILE_PATH)

def main():
    """Creates grid graphs that will be used in synthetic experiments.

    Each of these is a 12x12 grid where each unit has population 1
    and represents either one Democratic or one Republic vote.

    Creates nine maps total:
    three of these have 58 Republicans and 86 Democrats (approx. a 40% R–60% D split),
    three of these have 72 Republicans and 72 Democrats (a 50%-50% split),
    and three of these have 86 Republicans and 58 Democrats (approx. a 60% R–40% D split).

    Also creates .png images of these maps.
    """
    random_seed = 452
    random.seed(random_seed)
    
    create_blank_grid()

    for num_r_units in [72, 58, 86]:
        for map_number in [1, 2, 3]:
            create_dual_graph_image(num_r_units, map_number)

def assign_by_score(unit_dual_graph, num_r_units, score_func):
    scored = []

    for node, data in unit_dual_graph.nodes(data=True):
        i, j = data["old_node_index"]
        scored.append((score_func(i, j), node))

    scored.sort(reverse=True)

    unit_partisan_assignments = {}
    for k, (_, node) in enumerate(scored):
        unit_partisan_assignments[node] = 1 if k < num_r_units else 0

    return unit_partisan_assignments

def _finalize_and_save(graph, assignments, path):
    total_units = len(assignments)
    r_counter = sum(assignments.values())
    d_counter = total_units - r_counter

    for unit, data in graph.nodes(data=True):
        data['population'] = 1
        if assignments[unit] == 1:
            data['D'] = 0
            data['R'] = 1
        else:
            data['D'] = 1
            data['R'] = 0

    graph.to_json(path)

def create_blank_grid():
    unit_dual_graph = Graph.from_networkx(nx.grid_2d_graph(12,12))
    unit_dual_graph = Graph.from_networkx(nx.relabel.convert_node_labels_to_integers(unit_dual_graph, label_attribute ="old_node_index"))
    for unit, data in unit_dual_graph.nodes(data=True):
        data['population'] = 1

    save_grid_to = (
        f"{SCRIPT_DIR}/../syn_extra_unit_maps/"
        f"12x12_grid_no_votes.json"
    )
    os.makedirs(os.path.dirname(save_grid_to), exist_ok=True)
    unit_dual_graph.to_json(save_grid_to)

def create_clustered_dual_graph(num_r_units, map_number):
    """Creates .json files for maps described above.

    Args:
        num_r_units: number of Republican votes (58, 72, or 86)
        map_number: sample number out of maps with that partisan split (1, 2, or 3)
    """
    save_grid_maps_to = (
        f"{SCRIPT_DIR}/../syn_extra_unit_maps/map_.jsons/"
        f"clustered_r_units_{num_r_units}_map_{map_number}.json"
    )
    os.makedirs(os.path.dirname(save_grid_maps_to), exist_ok=True)
    
    # Create blank 12x12 grid
    unit_dual_graph = Graph.from_networkx(nx.grid_2d_graph(12,12))
    unit_dual_graph = Graph.from_networkx(nx.relabel.convert_node_labels_to_integers(unit_dual_graph, label_attribute ="old_node_index"))

    N = 12
    total_units = N * N

    # smooth random field → blobs
    noise = np.random.rand(N, N)
    smooth = gaussian_filter(noise, sigma=1.6)   # adjust sigma for cluster size

    # choose exactly num_r_units highest as R
    flat = smooth.flatten()
    cut = np.partition(flat, -num_r_units)[-num_r_units]

    grid_assign = (smooth >= cut).astype(int)  # 1 = R, 0 = D

    # build assignment dict keyed by node id
    unit_partisan_assignments = {}

    for node, data in unit_dual_graph.nodes(data=True):
        i, j = data["old_node_index"]   # original grid coordinate
        unit_partisan_assignments[node] = int(grid_assign[i, j])

    # -----------------------------
    # sanity checks
    # -----------------------------
    r_counter = sum(unit_partisan_assignments.values())
    d_counter = total_units - r_counter

    assert r_counter == num_r_units, "Wrong number of R units"
    assert d_counter == total_units - num_r_units, "Wrong number of D units"

    # -----------------------------
    # attach attributes to graph
    # -----------------------------
    for unit, data in unit_dual_graph.nodes(data=True):
        data['population'] = 1
        if unit_partisan_assignments[unit] == 1:
            data['D'] = 0
            data['R'] = 1
        else:
            data['D'] = 1
            data['R'] = 0

    unit_dual_graph.to_json(save_grid_maps_to)

def create_half_and_half_dual_graph(num_r_units, map_number):
    save_grid_maps_to = (
        f"{SCRIPT_DIR}/../syn_extra_unit_maps/map_.jsons/"
        f"half_r_units_{num_r_units}_map_{map_number}.json"
    )
    os.makedirs(os.path.dirname(save_grid_maps_to), exist_ok=True)

    unit_dual_graph = Graph.from_networkx(nx.grid_2d_graph(12,12))
    unit_dual_graph = Graph.from_networkx(
        nx.relabel.convert_node_labels_to_integers(
            unit_dual_graph, label_attribute="old_node_index"
        )
    )

    score = lambda i,j: -j   # left side first
    unit_partisan_assignments = assign_by_score(
        unit_dual_graph, num_r_units, score
    )

    _finalize_and_save(unit_dual_graph, unit_partisan_assignments, save_grid_maps_to)

def create_corners_dual_graph(num_r_units, map_number):
    save_grid_maps_to = (
        f"{SCRIPT_DIR}/../syn_extra_unit_maps/map_.jsons/"
        f"corners_r_units_{num_r_units}_map_{map_number}.json"
    )
    os.makedirs(os.path.dirname(save_grid_maps_to), exist_ok=True)

    unit_dual_graph = Graph.from_networkx(nx.grid_2d_graph(12,12))
    unit_dual_graph = Graph.from_networkx(
        nx.relabel.convert_node_labels_to_integers(
            unit_dual_graph, label_attribute="old_node_index"
        )
    )

    def corner_score(i,j):
        return -min(i+j, i+11-j, 11-i+j, 22-i-j)

    unit_partisan_assignments = assign_by_score(
        unit_dual_graph, num_r_units, corner_score
    )

    _finalize_and_save(unit_dual_graph, unit_partisan_assignments, save_grid_maps_to)

def create_checkerboard_dual_graph(num_r_units, map_number):
    save_grid_maps_to = (
        f"{SCRIPT_DIR}/../syn_extra_unit_maps/map_.jsons/"
        f"checkerboard_r_units_{num_r_units}_map_{map_number}.json"
    )
    os.makedirs(os.path.dirname(save_grid_maps_to), exist_ok=True)

    unit_dual_graph = Graph.from_networkx(nx.grid_2d_graph(12,12))
    unit_dual_graph = Graph.from_networkx(
        nx.relabel.convert_node_labels_to_integers(
            unit_dual_graph, label_attribute="old_node_index"
        )
    )

    def checker_score(i,j):
        return ((i+j) % 2) * 100 - (i+j)/100

    unit_partisan_assignments = assign_by_score(
        unit_dual_graph, num_r_units, checker_score
    )

    _finalize_and_save(unit_dual_graph, unit_partisan_assignments, save_grid_maps_to)

def create_bullseye_dual_graph(num_r_units, map_number):
    save_grid_maps_to = (
        f"{SCRIPT_DIR}/../syn_extra_unit_maps/map_.jsons/"
        f"bullseye_r_units_{num_r_units}_map_{map_number}.json"
    )
    os.makedirs(os.path.dirname(save_grid_maps_to), exist_ok=True)

    unit_dual_graph = Graph.from_networkx(nx.grid_2d_graph(12,12))
    unit_dual_graph = Graph.from_networkx(
        nx.relabel.convert_node_labels_to_integers(
            unit_dual_graph, label_attribute="old_node_index"
        )
    )

    def center_score(i,j):
        return -((i-5.5)**2 + (j-5.5)**2)

    unit_partisan_assignments = assign_by_score(
        unit_dual_graph, num_r_units, center_score
    )

    _finalize_and_save(unit_dual_graph, unit_partisan_assignments, save_grid_maps_to)

def create_striped_dual_graph(num_r_units, map_number):
    save_grid_maps_to = (
        f"{SCRIPT_DIR}/../syn_extra_unit_maps/map_.jsons/"
        f"striped_r_units_{num_r_units}_map_{map_number}.json"
    )
    os.makedirs(os.path.dirname(save_grid_maps_to), exist_ok=True)

    unit_dual_graph = Graph.from_networkx(nx.grid_2d_graph(12,12))
    unit_dual_graph = Graph.from_networkx(
        nx.relabel.convert_node_labels_to_integers(
            unit_dual_graph, label_attribute="old_node_index"
        )
    )

    def stripe_score(i,j):
        return -(j // 2) + i/100

    unit_partisan_assignments = assign_by_score(
        unit_dual_graph, num_r_units, stripe_score
    )

    _finalize_and_save(unit_dual_graph, unit_partisan_assignments, save_grid_maps_to)


def create_dual_graph_image(num_r_units, map_number):
    """Creates .png images for maps described above.

    Args:
        num_r_units: number of Republican votes (58, 72, or 86)
        map_number: sample number out of maps with that partisan split (1, 2, or 3)
    """
    save_grid_map_images_to = (
        f"{SCRIPT_DIR}/../syn_extra_unit_maps/map_.pngs/"
        f"half_r_units_{num_r_units}_map_{map_number}.png"
    )
    os.makedirs(os.path.dirname(save_grid_map_images_to), exist_ok=True)

    # Access appropriate dual graph .json file
    unit_dual_graph_json = (
        f"{SCRIPT_DIR}/../syn_extra_unit_maps/map_.jsons/"
        f"half_r_units_{num_r_units}_map_{map_number}.json"
    )

    unit_dual_graph = Graph.from_json(unit_dual_graph_json)
    
    # Create a 2D array in which each subarray is one row of the grid graph
    # Each subarray is 12 entries of either 1 (Dem vote) or 0 (Rep vote)
    grid_2D_array = []
    count = 0
    grid_row_array = []
    for unit, data in unit_dual_graph.nodes(data=True):
        if count != 12:
            grid_row_array.append(int(data['D']))
            count = count + 1
            if count == 12:
                grid_2D_array.append(grid_row_array)  
        else:
            count = 0
            grid_row_array = []
            grid_row_array.append(int(data['D']))
            count = 1
        
    # Use 2D array to create image of grid map
    grid_data = grid_2D_array
    cmap = matplotlib.colors.ListedColormap(['red', 'blue'])
    bounds = [0,1]
    norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)
    fig, ax = plt.subplots()
    ax.imshow(grid_data, cmap=cmap, norm=norm)
    ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
    ax.set_xticks(np.arange(-0.5, 12, 1))
    ax.set_yticks(np.arange(-0.5, 12, 1))
    ax.set_yticklabels([])
    ax.set_xticklabels([])

    plt.savefig(save_grid_map_images_to)

main()


