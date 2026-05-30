import os
import networkx as nx
from gerrychain import Graph
from gerrychain.partition import Partition

SCRIPT_FILE_PATH = os.path.abspath(__file__)
SCRIPT_DIR = os.path.dirname(SCRIPT_FILE_PATH)

def make_block_size_1_building_blocks():
    block_size = 1
    n_samples = 100

    grid_dual_graph_file = f"{SCRIPT_DIR}/../syn_files/syn_unit_maps/12x12_grid_no_votes.json"
    grid_graph = Graph.from_json(grid_dual_graph_file)

    # Each node is its own district
    district_units_dict = {i: {i} for i in grid_graph.nodes}

    # Create quotient graph (will be identical to original)
    subgraph = nx.quotient_graph(grid_graph, list(district_units_dict.values()))
    subgraph = nx.convert_node_labels_to_integers(subgraph)
    neutral_subgraph = Graph.from_networkx(subgraph)

    # Add node attributes in the same style as your other building block graphs
    for node, data in neutral_subgraph.nodes(data=True):
        units = data["graph"].nodes
        neutral_subgraph.nodes[node]["units"] = str(units)
        neutral_subgraph.nodes[node]["population"] = block_size
        neutral_subgraph.nodes[node]["id"] = '"' + str(node) + '"'

    # Save 100 identical samples
    for i in range(n_samples):
        save_to_file = (
            f"{SCRIPT_DIR}/../syn_files/syn_building_block_partitions/neutral/"
            f"block_size_{block_size}/sample_{i+1}.json"
        )
        os.makedirs(os.path.dirname(save_to_file), exist_ok=True)
        neutral_subgraph.to_json(save_to_file)
        print(f"Saved sample {i+1} for block size 1")

# Call the function
make_block_size_1_building_blocks()