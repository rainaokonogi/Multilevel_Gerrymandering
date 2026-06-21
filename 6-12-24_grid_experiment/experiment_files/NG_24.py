from gerrychain import (Partition, Graph, MarkovChain, updaters, accept, Election)
from gerrychain.proposals import recom
from gerrychain.tree import recursive_tree_part
from gerrychain.constraints import contiguous
from gerrychain.optimization import Gingleator
from functools import partial
import random
import ast
import os
from pyben import PyBenEncoder
import jsonlines as jl

CURRENT_WORKING_DIRECTORY = Path.cwd()

def safe_reward_partial_dist_v2(part, minority_perc_col, threshold=0.5):
    """Score function that returns the number of districts won by the party being
    gerrymandered toward + 0.5 * the number of tied districts + the highest percentage of
    votes that party receives in any losing district.

    As opposed to the reward_partial_dist function currently in GerryChain, this function doesn't throw an
    error if no districts are below threshold. If no such district exists, returns just wins + ties.
    
    Args:
        part (Partition): GerryChain Partition object.
        minority_perc_col (str): Column name for gerrymandering party's votes.
        threshold (float): Threshold for winning a district.
    """
    try:
        dist_percs = part[minority_perc_col].values()
        num_win_dists = sum(list(map(lambda v: v > threshold, dist_percs)))
        num_tie_dists = sum(list(map(lambda v: v == threshold, dist_percs)))
        next_dist = max(i for i in dist_percs if i < threshold)
        return (num_win_dists + (0.5 * num_tie_dists) + next_dist)
    except ValueError:
        num_win_dists = sum(list(map(lambda v: v > threshold, dist_percs)))
        num_tie_dists = sum(list(map(lambda v: v == threshold, dist_percs)))
        return (num_win_dists + num_tie_dists)


def run_experiment_ng(num_r_units, block_size, init_part, random_seed, burst_length, total_steps):
    """Run experiment where the building blocks are not gerrymandered but the resulting map is.

    Args:
        num_r_units (int): Number of Republican units in underlying map (e.g., 18, 21).
        block_size (int): Size of building blocks (e.g., 1, 2, 3).
        init_part (int): Number of initial district partition to use for Markov chain (1–3)
        random_seed (int): Random seed for reproducibility.
        party (str): the party being gerrymandered toward — either "D" for blue party or "R" for red party.
        burst_length (int): Burst length for short bursts algorithm.
        total_steps (int): Total number of steps for each chain (must be divisible by burst length).
    """

    # Load data from underlying map as graph
    # Will use this to put vote totals onto block graph
    underlying_map = (
        f"{CURRENT_WORKING_DIRECTORY}/6-12-24_grid_experiment/grids_and_blocks/grid_maps/24x24_units_maps/grids_.jsons/"
        f"med_BR_score_r_units_{num_r_units}_map_1.json"
    )
    underlying_graph = Graph.from_json(underlying_map)

    # Set pop data, random seed
    random.seed(random_seed)
    pop_col = 'population'

    # Iterate over building block files
    for sample in range(1,101):

        save_assignment_results_to = (
            f"{CURRENT_WORKING_DIRECTORY}/REP_DATA_(replicated)/6-12-24_grid_results_(replicated)/24x24_grid_results/NG/output_ensembles/toward_{party}/med_BR_score_r_units_{num_r_units}_map_1/block_size_{block_size}/"
            f"sample_{sample}/init_part_{init_part}_random_seed_{random_seed}_burst_length_{burst_length}_steps_{total_steps}_assignment.ben"
        )
        save_updaters_results_to = (
            f"{CURRENT_WORKING_DIRECTORY}/REP_DATA_(replicated)/6-12-24_grid_results_(replicated)/24x24_grid_results/NG/output_updaters/toward_{party}/med_BR_score_r_units_{num_r_units}_map_1/block_size_{block_size}/"
            f"sample_{sample}/init_part_{init_part}_random_seed_{random_seed}_burst_length_{burst_length}_steps_{total_steps}_updaters.jsonl"
        )
        os.makedirs(os.path.dirname(save_assignment_results_to), exist_ok=True)
        os.makedirs(os.path.dirname(save_updaters_results_to), exist_ok=True)

        block_data = (
            f"{CURRENT_WORKING_DIRECTORY}/6-12-24_grid_experiment/grids_and_blocks/24_block_partitions/"
            f"block_size_{block_size}/sample_{sample}.json"
        )

        block_graph = Graph.from_json(block_data)

        # For use later when saving results
        graph_node_order = list(block_graph.nodes)

        # Use data from underlying map to add vote totals for each building block to block graph
        block_to_nodes_dict = {}

        for block, data in block_graph.nodes(data=True):
            if "units" in data:
                block_to_nodes_dict[block] = ast.literal_eval(data["units"])

        for block in block_graph.nodes:
            d_votes = 0
            r_votes = 0
            nodes_in_block = block_to_nodes_dict[block]
            for node in nodes_in_block:
                d_votes = d_votes + underlying_graph.nodes[node]['D']
                r_votes = r_votes + underlying_graph.nodes[node]['R']
            block_graph.nodes[block]['D'] = d_votes
            block_graph.nodes[block]['R'] = r_votes

        # Updaters
        my_updaters = {
            "population": updaters.Tally("population",alias="population"),
            "election": Election("election", {"D": "D", "R": "R"}),
            "R_tally": updaters.Tally("R",alias="R_tally"),
            "D_tally": updaters.Tally("D",alias="D_tally"),
            }

        # Pull initial partition from block graph
        initial_partition = Partition(
            block_graph,
            assignment=f"init_part_{init_part}",
            updaters=my_updaters
        )

        # 576 nodes and 6 districts, so pop_target is 96
        proposal = partial(
            recom,
            pop_col=pop_col,
            pop_target=96,
            epsilon=0,
            node_repeats=2
        )

        # Define recom chain
        # Gingleator score function should return number of districts where over 50% of the votes go to gerrymandered party
        # + percentage of that party in district where it gets the highest vote share under 50%
        recom_chain = Gingleator(
            proposal=proposal,
            constraints=[contiguous],
            threshold=0.5,
            initial_state=initial_partition,
            total_pop_col='population',
            minority_pop_col=f'{party}_tally',
            score_function=safe_reward_partial_dist_v2
        )

        # Save results
        with (
                PyBenEncoder(save_assignment_results_to, overwrite=True) as encoder,
                jl.open(save_updaters_results_to, "w") as updater_output_file,
            ):
        
            for i, plan in enumerate(recom_chain.short_bursts(burst_length,round(total_steps/burst_length))):

                assert (
                    plan is not None
                ), "Something went terribly wrong. There is no output partition."

                assignment_series = plan.assignment.to_series()
                ordered_assignment = (
                    assignment_series.loc[graph_node_order].astype(int).tolist()
                )
                encoder.write(ordered_assignment)

                election = plan["election"]
                
                seats_won = {
                    "D": election.seats("D"),
                    "R": election.seats("R")
                }

                regions = election.regions 

                d_counts = election.counts("D")
                r_counts = election.counts("R")
                d_votes_by_district = dict(zip(regions, d_counts))
                r_votes_by_district = dict(zip(regions, r_counts))

                district_winners = {region: ("D" if d > r else "R") for region, d, r in zip(regions, d_counts, r_counts)}

                record = {
                    "step": i,
                    "population": dict(plan["population"]),
                    "Seats won": seats_won,
                    "D votes": d_votes_by_district,
                    "R votes": r_votes_by_district,
                    "District winners": district_winners
                }

                updater_output_file.write(record)