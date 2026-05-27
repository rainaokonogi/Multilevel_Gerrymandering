import networkx as nx
import numpy as np
import random
import os
from gerrychain import Graph
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.colors import ListedColormap, BoundaryNorm
from scipy.ndimage import gaussian_filter

save_grid_map_images_to = f"/share/duchin/raina/syn_files/unit_maps_to_use/map_.pngs/low_BR_score_r_units_86_map_3.png"
os.makedirs(os.path.dirname(save_grid_map_images_to), exist_ok=True)

unit_dual_graph_json = f"/share/duchin/raina/syn_files/unit_maps_to_use/map_.jsons/low_BR_score_r_units_86_map_3.json"
unit_dual_graph = Graph.from_json(unit_dual_graph_json)

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
cmap = matplotlib.colors.ListedColormap(['#E62020', '#1560BD'])
bounds = [0,1]
norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)
fig, ax = plt.subplots()
ax.imshow(grid_data, cmap=cmap, norm=norm)
ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
ax.set_xticks(np.arange(-0.5, 12, 1))
ax.set_yticks(np.arange(-0.5, 12, 1))
ax.set_yticklabels([])
ax.set_xticklabels([])
plt.tight_layout()
plt.savefig(save_grid_map_images_to, bbox_inches='tight')