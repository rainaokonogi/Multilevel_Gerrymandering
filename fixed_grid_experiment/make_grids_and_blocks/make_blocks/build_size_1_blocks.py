import os
import networkx as nx
from gerrychain import Graph
from gerrychain.partition import Partition
from pathlib import Path

CURRENT_WORKING_DIRECTORY = Path.cwd()

def main():
    """Creates 100 copies of the grid saved in the same format as the other building block partitions,
    for use when running the experiments with building block size 1.
    """

    block_size = 1
    n_samples = 100

    # Load 12x12 grid
    grid_dual_graph_file = f"{CURRENT_WORKING_DIRECTORY}/fixed_grid_experiment/grids_and_blocks/grid_maps/grids_.jsons/12x12_grid_no_votes.json"
    grid_graph = Graph.from_json(grid_dual_graph_file)

    # Each node is its own district
    district_units_dict = {i: {i} for i in grid_graph.nodes}

    # Create quotient graph (will be identical to original)
    subgraph = nx.quotient_graph(grid_graph, list(district_units_dict.values()))
    subgraph = nx.convert_node_labels_to_integers(subgraph)
    neutral_subgraph = Graph.from_networkx(subgraph)

    # Add node attributes in the same style as other building block graphs
    for node, data in neutral_subgraph.nodes(data=True):
        units = data["graph"].nodes
        neutral_subgraph.nodes[node]["units"] = str(units)
        neutral_subgraph.nodes[node]["population"] = block_size
        neutral_subgraph.nodes[node]["id"] = '"' + str(node) + '"'

    # Save 100 identical samples
    for i in range(n_samples):
        save_location = (
            f"{CURRENT_WORKING_DIRECTORY}/fixed_grid_experiment/grids_and_blocks_(replicated)/block_partitions"
            f"/block_size_{block_size}/sample_{i+1}.json"
        )
        os.makedirs(os.path.dirname(save_location), exist_ok=True)
        neutral_subgraph.to_json(save_location)
        print(f"Saved sample {i+1} for block size 1")

main()