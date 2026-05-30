import numpy as np
import random
from gerrychain import Graph
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.colors import ListedColormap, BoundaryNorm
import networkx as nx
import os

# FOR 72-72:

# random_seed_1 = 45
# random_seed_2 = 37
# random_seed_3 = 91
# random_seed_4 = 12
# random_seed_5 = 81
# random_seed_6 = 3

# FOR 86 R-58 B:

# random_seed_1 = 56
# random_seed_2 = 67
# random_seed_3 = 21
# random_seed_4 = 22
random_seed = 100

random.seed(random_seed)
np.random.seed(random_seed)

N = 12
NUM_NODES = N * N

neighbors = {}
for r in range(N):
    for c in range(N):
        i = r * N + c
        nbrs = []
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < N and 0 <= nc < N:
                nbrs.append(nr * N + nc)
        neighbors[i] = nbrs


grid = np.array([0]*58 + [1]*86) # CHANGE HERE TO CHANGE NUMBER BLUE, RED
np.random.shuffle(grid)

def cut_edges(grid):
    count = 0
    for i in range(NUM_NODES):
        for j in neighbors[i]:
            if i < j and grid[i] != grid[j]:
                count += 1
    return count


def delta_swap(grid, i, j):
    if grid[i] == grid[j]:
        return 0

    delta = 0

    for u in (i, j):
        for v in neighbors[u]:
            if v == i or v == j:
                continue

            before = (grid[u] != grid[v])
            after = ((1 - grid[u]) != grid[v])

            delta += int(after) - int(before)

    return delta


score = cut_edges(grid)

for step in range(20000):

    reds = np.where(grid == 1)[0]
    blues = np.where(grid == 0)[0]

    i = random.choice(reds)
    j = random.choice(blues)

    d = delta_swap(grid, i, j)
    new_score = score + d

    # accept if better (or sometimes randomly)
    if new_score > score:
        accept = True
    else:
        accept = random.random() < 0.01  # small noise

    if accept:
        grid[i], grid[j] = grid[j], grid[i]
        score = new_score

    if step % 2000 == 0:
        print(step, score)

print("\nFinal cut edges:", score)

G = Graph.from_networkx(nx.grid_2d_graph(12,12))
G = Graph.from_networkx(nx.relabel.convert_node_labels_to_integers(G, label_attribute ="old_node_index"))

# attach attributes
for i in G.nodes():
    G.nodes[i]["R"] = int(grid[i] == 1)
    G.nodes[i]["D"] = int(grid[i] == 0)

save_grid_maps_to = (
    f"/share/duchin/raina/syn_files/syn_unit_maps_extra/map_.jsons/high_diff_edges_r_units_86_map_5.json"
)
save_grid_map_images_to = (
    f"/share/duchin/raina/syn_files/syn_unit_maps_extra/map_.pngs/high_diff_edges_r_units_86_map_5.png"
)
os.makedirs(os.path.dirname(save_grid_maps_to), exist_ok=True)
os.makedirs(os.path.dirname(save_grid_map_images_to), exist_ok=True)


grid_2D_array = []
count = 0
grid_row_array = []
for unit, data in G.nodes(data=True):
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

plt.savefig(save_grid_map_images_to)

G.to_json(save_grid_maps_to)