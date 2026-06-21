from gerrychain import Partition, Graph, updaters
from gerrychain.tree import recursive_tree_part
import random
import os
from networkx.readwrite import json_graph
from pathlib import Path
import json

CURRENT_WORKING_DIRECTORY = Path.cwd()

random_seed_num = 320
random.seed(random_seed_num)

def main():
    """
    For each size 1 building block graph, finds three initial partitions (assignments of blocks to districts).
    Creates a new block graph where these initial partition are saved as
    node attributes "init_part_1", "init_part_2", and "init_part_3".
    Saves in the "grids_and_blocks_(replicated)" folder; if you have already made the building block graph there,
    it overwrites that.
    """

    neutral_blocks_dir = (
            f"{CURRENT_WORKING_DIRECTORY }/fixed_grid_experiment/grids_and_blocks/block_partitions/neutral/block_size_1"
        )

    file_count = 0

    # Iterate over each size 1 building block graph
    for json_file in Path(neutral_blocks_dir).rglob("*.json"):
        file_count += 1

        if file_count % 10 == 0:
            print(f"Processed {file_count} files (out of 100)")

        file_name = f"{neutral_blocks_dir}/{json_file.name}"

        graph = Graph.from_json(file_name)

        my_updaters = {
            "population": updaters.Tally("population",alias="population"),
            "R_tally": updaters.Tally("R",alias="R_tally"),
            "D_tally": updaters.Tally("D",alias="D_tally")
            }

        # Find three initial partitions
        for i in [1,2,3]:
            n_found = 0
            while n_found < 1:
                try:
                    init_part_i = Partition.from_random_assignment(
                        graph=graph,
                        n_parts=12,
                        pop_col='population',
                        updaters = my_updaters,
                        epsilon = 0.00001,
                        method = recursive_tree_part
                    )
                    n_found += 1
                except Exception:
                    pass
            
            assignment_i = init_part_i.assignment

            for block, district in assignment_i.items():
                graph.nodes[block][f"init_part_{i}"] = district

        # Saves in the "grids_and_blocks_(replicated)" folder.
        # If there is already a building block graph without initial partitions in that folder, it overwrites.
        save_location = (
            f"{CURRENT_WORKING_DIRECTORY}/fixed_grid_experiment/grids_and_blocks_(replicated)/block_partitions"
            f"/block_size_1/sample_{i+1}.json"
        )
        os.makedirs(os.path.dirname(save_location), exist_ok=True)
        
        with open(save_location, "w") as f:
            json.dump(json_graph.adjacency_data(graph), f)

main()