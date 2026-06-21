import os
import json
import ast
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from pathlib import Path

CURRENT_WORKING_DIRECTORY = Path.cwd()

def make_building_block_partition_image(assort_score, num_r_units, map_number, block_size, sample_number):
    """For a given grid and building block partition, creates an image of the grid with units colored red or blue
    and with building blocks outlined in yellow.

    Args:
    map_type: "high", "low", or "med", inidicating assoratativity variable.
    num_r_units: "72" or "86", indicatating partisanship variable.
    map_number: "1", "2", or "3", indicating choice of map variable.
    block_size: "1", "2", "3", "4", or "6", number of units in each building block.
    sample_number: "1", "2", ..., or "100", indicating choice of building block partition.
    """
    unit_assignments = f"{CURRENT_WORKING_DIRECTORY}/fixed_grid_experiment/grids_and_blocks/grid_maps/grids_.jsons/{assort_score}_BR_score_r_units_{num_r_units}_map_{map_number}.json"
    block_assignments = f"{CURRENT_WORKING_DIRECTORY}/fixed_grid_experiment/grids_and_blocks/block_partitions/neutral/block_size_{block_size}/sample_{sample_number}.json"

    save_location = f"{CURRENT_WORKING_DIRECTORY}/image_replication/building_block_partition_example_images/{assort_score}_BR_score_r_units_{num_r_units}_map_{map_number}_block_size_{block_size}_sample_{sample_number}_image.png"
    os.makedirs(os.path.dirname(save_location), exist_ok=True)

    # Load grid data
    with open(unit_assignments, 'r') as f:
        unit_data = json.load(f)

    # Create a 2D array storing partisan assignments for each row of our 12x12 grid
    grid_2D_array = []
    count = 0
    empty_array = []

    for node in unit_data["nodes"]:
        if count != 12:
            empty_array.append(int(node["D"]))
            count += 1
            if count == 12:
                grid_2D_array.append(empty_array)
        else:
            count = 0
            empty_array = [int(node["D"])]
            count = 1

    # Load block partition data
    with open(block_assignments, 'r') as f:
        block_data = json.load(f)

    # Create a dictionary storing each unit in the grid and its block assignment in the building block partition
    label_grid = {}
    for block in block_data["nodes"]:
        units_list = ast.literal_eval(block["units"])
        for unit in units_list:
            label_grid[unit] = block["id"]

    sorted_dict = dict(sorted(label_grid.items()))
    new_array = list(sorted_dict.values())
    blocks = np.array(new_array).reshape((12, 12))

    # Plot image
    data = grid_2D_array
    cmap = matplotlib.colors.ListedColormap(['#E62020', '#1560BD'])
    bounds = [0, 1]
    norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)

    fig, ax = plt.subplots()
    ax.imshow(data, cmap=cmap, norm=norm, zorder=0)

    # Fix alignment
    ax.set_xlim(-0.5, 11.5)
    ax.set_ylim(11.5, -0.5)
    ax.set_aspect('equal')

    # Remove outer black border
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Grid using minor ticks
    ax.set_xticks(np.arange(-0.5, 12, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, 12, 1), minor=True)
    ax.grid(which='minor', color='black', linewidth=1, zorder=1)

    # Remove tick labels
    ax.set_xticks([])
    ax.set_yticks([])

    # District boundaries (yellow)
    for y in range(12):
        for x in range(12):
            current = blocks[y, x]

            if x < 11 and blocks[y, x+1] != current:
                ax.plot([x+0.5, x+0.5], [y-0.5, y+0.5],
                        color='#FFFFC5', linewidth=2.0, zorder=2)

            if y < 11 and blocks[y+1, x] != current:
                ax.plot([x-0.5, x+0.5], [y+0.5, y+0.5],
                        color='#FFFFC5', linewidth=2.0, zorder=2)

            if y == 0:
                ax.plot([x-0.5, x+0.5], [y-0.5, y-0.5],
                        color='#FFFFC5', linewidth=2.0, zorder=2)

            if x == 0:
                ax.plot([x-0.5, x-0.5], [y-0.5, y+0.5],
                        color='#FFFFC5', linewidth=2.0, zorder=2)

    # Outer border
    outer_rect = plt.Rectangle(
        (-0.5, -0.5),
        12,
        12,
        edgecolor='#FFFFC5',
        facecolor='none',
        linewidth=4.0,
        zorder=3
    )
    ax.add_patch(outer_rect)

    plt.savefig(save_location, dpi=300, bbox_inches='tight')

def main():
    """Makes the four block partition example images shown in the paper.
    """
    assort_score = "med"
    num_r_units = 72
    map_number = 1
    sample_number = 1

    for block_size in [2, 3, 4, 6]:
        make_building_block_partition_image(assort_score, num_r_units, map_number, block_size, sample_number)

main()