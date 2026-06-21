import networkx as nx
from networkx.readwrite import json_graph
import json
from gerrychain import Graph
from pathlib import Path
import os

CURRENT_WORKING_DIRECTORY = Path.cwd()

def collapse_zero_pop_nodes(G):
    """
    Take a Gerrychain graph object. Identify any node with zero Democratic and zero Republican votes.
    Then, merge this node with its neighbor with the most total votes by creating an edge between
    any neighbor of the original node and said largest neighbor.
    The goal is to be able to use these graphs to create Moran's I scatter plots.

    Args:
        G (Gerrychain graph object): the graph you wish to modify.
    """
    G = G.copy()

    def total_pop(n):
        return G.nodes[n].get("total_pop")
    
    zero_pop_nodes = []
    for node, data in G.nodes(data=True):
        if total_pop(node) == 0:
            zero_pop_nodes.append(node)
    
    for node in zero_pop_nodes:
        
        neighbors = list(G.neighbors(node))
        if not neighbors:
            G.remove_node(node)
            print("Removed an island!")
            continue

        biggest_neighbor = max(neighbors, key=total_pop)
        
        for neighbor in neighbors:
            if neighbor != biggest_neighbor:
                G.add_edge(biggest_neighbor, neighbor)
        
        G.remove_node(node)
    
    return G

# Pre-process all Montana dual graphs
for block_type in ["vtds", "blockgroups", "tracts", "counties"]:
    mt_dual_graph = f"{CURRENT_WORKING_DIRECTORY}/MT_files/dual_graphs/MT_{block_type}_dual_graph.json"
    
    G = Graph.from_json(mt_dual_graph)

    G_pres = collapse_zero_pop_nodes(G)
    G_sen = collapse_zero_pop_nodes(G)

    save_location = f"{CURRENT_WORKING_DIRECTORY}/MT_files/dual_graphs/morans_i_graphs/white_v_nonwhite/MT_{block_type}_dual_graph_for_moran.json"
    save_location = f"{CURRENT_WORKING_DIRECTORY}/MT_files/dual_graphs/morans_i_graphs/white_v_nonwhite/MT_{block_type}_dual_graph_for_moran.json"
    os.makedirs(os.path.dirname(save_location), exist_ok=True)

    G_pres.to_json(save_location)
    G_sen.to_json(save_location)