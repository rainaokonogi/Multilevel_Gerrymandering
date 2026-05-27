import geopandas as gpd
import gerrychain
import matplotlib
import os
import matplotlib.pyplot as plt
import networkx as nx
import functools
import json
import pandas as pd
from matplotlib.patches import Patch
from pathlib import Path

CURRENT_WORKING_DIRECTORY = Path.cwd()

@functools.cache  # cached for speed purposes
def _angle_1(graph: gerrychain.Graph, x_col: str, y_col: str) -> float:
    first_summation = 0
    second_summation = 0
    for node in graph.nodes():
        first_summation += int(graph.nodes[node][x_col]) * int(graph.nodes[node][y_col])

    for u,v in graph.edges():
        second_summation += int(graph.nodes[u][x_col]) * int(
            graph.nodes[v][y_col]
        )
        second_summation += int(graph.nodes[v][x_col]) * int(
            graph.nodes[u][y_col]
        )

    return (first_summation, second_summation)

def angle_1(graph: gerrychain.Graph, x_col: str, y_col: str, lam: float = 1) -> float:
    """
    This implements `<x_col, y_col>` from the paper that introduces CAPY scores
    """
    first_summation, second_summation = _angle_1(graph, x_col, y_col)

    if lam == None:
        return first_summation
    else:
        return (lam * first_summation) + second_summation

@functools.cache
def _angle_2(graph: gerrychain.Graph, x_col: str, y_col: str, lam: float = 1) -> float:
    first_summation = 0
    second_summation = 0
    for node in graph.nodes():
        first_summation += int(graph.nodes[node][x_col]) * int(
            graph.nodes[node][y_col]
        ) - ((int(graph.nodes[node][x_col]) + int(graph.nodes[node][y_col])) * 0.5)

    for u,v in graph.edges():
        second_summation += int(graph.nodes[u][x_col]) * int(
            graph.nodes[v][y_col]
        )
        second_summation += int(graph.nodes[v][x_col]) * int(
            graph.nodes[u][y_col]
        )

    return (first_summation, second_summation)

def angle_2(graph: gerrychain.Graph, x_col: str, y_col: str, lam: float = 1) -> float:
    """
    This implements `<<x_col, y_col>>` from the paper that introduces CAPY scores
    """
    first_summation, second_summation = _angle_2(graph, x_col, y_col)

    if lam == None:
        return first_summation
    else:
        return 0.5 * ((lam * first_summation) + second_summation)

def half_edge(
    graph: gerrychain.Graph, x_col: str, y_col: str, lam: float = 1, func=angle_1
) -> float:
    x_x = func(graph, x_col, x_col, lam=lam)
    x_y = func(graph, x_col, y_col, lam=lam)
    y_y = func(graph, y_col, y_col, lam=lam)

    return 0.5 * ((x_x / (x_x + x_y)) + (y_y / (y_y + x_y)))

for block_type in ["vtds", "blockgroups", "tracts", "counties"]:

    graph_json = f"{CURRENT_WORKING_DIRECTORY}/REPLICATION_REPO/NY_files/dual_graphs/NY_{block_type}_dual_graph.json"

    if block_type == "vtds":
        shp_path = f"{CURRENT_WORKING_DIRECTORY}/REPLICATION_REPO/NY_files/shapefiles/vtds_shapefiles/tl_2020_30_vtd20_with_pop_election.shp"
    elif block_type == "blockgroups":
        shp_path = f"{CURRENT_WORKING_DIRECTORY}/REPLICATION_REPO/NY_files/shapefiles/blockgroups_shapefiles/tl_2020_30_bg_with_pop_election.shp"
    elif block_type == "tracts":
        shp_path = f"{CURRENT_WORKING_DIRECTORY}/REPLICATION_REPO/NY_files/shapefiles/tracts_shapefiles/tl_2020_30_tract_with_pop_election.shp"
    elif block_type == "counties":
        shp_path = f"{CURRENT_WORKING_DIRECTORY}/REPLICATION_REPO/NY_files/shapefiles/counties_shapefiles/ny_counties_with_race_election.shp"

    # Load shapefile
    gdf = gpd.read_file(shp_path)

    # Build Graph from JSON
    graph = Graph.from_json(graph_json)

    # Compute pop_diff for each node
    for node in graph.nodes:
        total_pop = graph.nodes[node].get("total_pop", 0)
        white_pop = graph.nodes[node].get("white_pop", 0)
        graph.nodes[node]['non_white_pop'] = total_pop - white_pop

    # Compute half-edge score
    ny_CAPY_result = half_edge(graph, "white_pop", "non_white_pop")

    # Reproject shapefile for positions
    # Montana: 26912
    # NY: 2263
    gdf = gdf.to_crs(epsg=2263)
    centroids = gdf.geometry.centroid

    # Map GEOID → position
    # Build GEOID → position dictionary from gdf
    gdf_geoid_to_pos = {row["GEOID"]: (row.geometry.centroid.x, row.geometry.centroid.y)
                        for _, row in gdf.iterrows()}

    # Build node → position mapping
    # Check if nodes have 'GEOID' attribute
    pos = {}
    for node in graph.nodes:
        geoid = graph.nodes[node].get("GEOID")  # each node should have GEOID
        if geoid is None:
            raise ValueError(f"Node {node} has no GEOID attribute!")
        pos[node] = gdf_geoid_to_pos[geoid]


    node_colors = []
    node_maj = {}
    for node in graph.nodes:
        white = graph.nodes[node]['white_pop']
        nonwhite = graph.nodes[node]['non_white_pop']
        if white > nonwhite:
            node_colors.append(colors[0])
            node_maj[node] = "white"
        elif nonwhite > white:
            node_colors.append(colors[1]) 
            node_maj[node] = "nonwhite"
        else:
            node_colors.append("gray")
            node_maj[node] = "TIE"

    plt.figure(figsize=(10, 8))

    nx.draw_networkx_edges(
        graph,
        pos,
        edge_color="black",
        width=0.4
    )

    node_sizes = [graph.nodes[n]['total_pop'] for n in graph.nodes]

    node_sizes = [size * 0.02 for size in node_sizes]

    nx.draw_networkx_nodes(
        graph,
        pos,
        node_size=node_sizes,
        node_color=node_colors
    )
    legend_elements = [
        Patch(facecolor="#1560BD", edgecolor="#1560BD", label="Majority White"),
        Patch(facecolor="#E62020", edgecolor="#E62020", label="Majority Non-White")
    ]
    plt.axis("equal")
    plt.axis("off")
    plt.margins(0)
    plt.tight_layout()
    plt.suptitle(
        "half-edge score = " + str(ny_CAPY_result),
        fontsize=20
    )
    save_location = f"{CURRENT_WORKING_DIRECTORY}/image_replication/NY_race_CAPY_images/white_vs_non_white_{block_type}.png"
    os.makedirs(save_location, exist_ok=True)
    plt.savefig(save_location, dpi=600)
    plt.close()