import networkx as nx
import numpy as np
import random
import os
from gerrychain import Graph
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.colors import ListedColormap, BoundaryNorm
from scipy.ndimage import gaussian_filter

def create_blank_grid():
    unit_dual_graph = Graph.from_networkx(nx.grid_2d_graph(24,24))
    unit_dual_graph = Graph.from_networkx(nx.relabel.convert_node_labels_to_integers(unit_dual_graph, label_attribute ="old_node_index"))
    for unit, data in unit_dual_graph.nodes(data=True):
        data['population'] = 1

    save_grid_to = (
        f"/share/duchin/raina/6-12-24_grid_exp/24x24_unit_maps/map_.jsons/24_by_24_grid_no_votes.json"
    )
    os.makedirs(os.path.dirname(save_grid_to), exist_ok=True)
    unit_dual_graph.to_json(save_grid_to)

create_blank_grid()