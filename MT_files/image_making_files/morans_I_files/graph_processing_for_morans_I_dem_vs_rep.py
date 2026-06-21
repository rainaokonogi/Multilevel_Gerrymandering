import networkx as nx
from networkx.readwrite import json_graph
import json
from gerrychain import Graph
from pathlib import Path
import os

CURRENT_WORKING_DIRECTORY = Path.cwd()

def collapse_zero_vote_nodes(G, election):
    """
    Take a Gerrychain graph object. Identify any node with zero Democratic and zero Republican votes.
    Then, merge this node with its neighbor with the most total votes by creating an edge between
    any neighbor of the original node and said largest neighbor.
    The goal is to be able to use these graphs to create Moran's I scatter plots.

    Args:
        G (Gerrychain graph object): the graph you wish to modify.
        election (str): relevant election data (should be "PRES20" or "SEN20" for Montana; "PRES20" or "SEN22" for New York)
    """
    G = G.copy()

    dem_votes = f"{election}DEM"
    rep_votes = f"{election}REP"

    def total_votes(n):
        return G.nodes[n].get(dem_votes) + G.nodes[n].get(rep_votes)
    
    zero_vote_nodes = []
    for node, data in G.nodes(data=True):
        if total_votes(node) == 0:
            zero_vote_nodes.append(node)
    
    for node in zero_vote_nodes:
        
        neighbors = list(G.neighbors(node))
        if not neighbors:
            G.remove_node(node)
            print("Removed an island!")
            continue

        biggest_neighbor = max(neighbors, key=total_votes)
        
        for neighbor in neighbors:
            if neighbor != biggest_neighbor:
                G.add_edge(biggest_neighbor, neighbor)
        
        G.remove_node(node)
    
    return G

# Pre-process all Montana dual graphs
for block_type in ["vtds", "blockgroups", "tracts", "counties"]:
    mt_dual_graph = f"{CURRENT_WORKING_DIRECTORY}/MT_files/dual_graphs/MT_{block_type}_dual_graph.json"
    
    G = Graph.from_json(mt_dual_graph)

    G_pres = collapse_zero_vote_nodes(G, "PRES20")
    G_sen = collapse_zero_vote_nodes(G, "SEN20")

    pres_save_location = f"{CURRENT_WORKING_DIRECTORY}/MT_files/dual_graphs/morans_i_graphs/dem_v_rep/MT_{block_type}_dual_graph_pres_for_moran.json"
    sen_save_location = f"{CURRENT_WORKING_DIRECTORY}/MT_files/dual_graphs/morans_i_graphs/dem_v_rep/MT_{block_type}_dual_graph_sen_for_moran.json"
    os.makedirs(os.path.dirname(pres_save_location), exist_ok=True)

    G_pres.to_json(pres_save_location)
    G_sen.to_json(sen_save_location)