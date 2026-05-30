from gerrychain import Partition, Graph, updaters, Election
from gerrychain.proposals import recom
from gerrychain.tree import bipartition_tree
from gerrychain.constraints import contiguous
from gerrychain.optimization import Gingleator
from functools import partial
import random
import jsonlines as jl
import os
from pyben import PyBenEncoder
import json
from pathlib import Path

CURRENT_WORKING_DIRECTORY = Path.cwd()

def safe_reward_partial_dist(part, minority_perc_col, threshold=0.5):
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
        return (num_win_dists + (0.5 * num_tie_dists))

def MT_gerry_exp(block_type, election, party, init_part, random_seed, burst_length, total_steps):
    """Runs one optimized search of Montana redistricting plans.

    Args:
        block_type (str): type of census unit being aggregated into districts (blockgroups, VTDs, or tracts).
        election (str): choice of election data used to determine winners of districts,
            either "pres" for the 2020 Presidential election or "sen" for the 2020 U.S. Senate election.
        party (str): party being gerrymandered toward, either "D" for Democrats or "R" for Republicans.
        init_part (int): Number of initial partition into districts to use for Markov chain (1–5)
        random_seed (int): Random seed for reproducibility.
        burst_length (int): Number of plans in one "burst" as defined by short bursts optimization method.
        total_steps (int): Total number of steps for the chain; must be divisible by the burst length.
    """

    # Load dual graph of census units
    dual_graph_info = (
        f"{CURRENT_WORKING_DIRECTORY}/"
        f"/MT_files/dual_graphs/"
        f"MT_{block_type}_dual_graph.json"
    )
    dual_graph = Graph.from_json(dual_graph_info)

    # For use later when saving results
    graph_node_order = list(dual_graph.nodes)

    # Create files to store new results; shouldn't overwrite results already in folder
    save_assignment_results_to = (
        f"{CURRENT_WORKING_DIRECTORY}/MT_results_(replicated)/gerry/gerry_ensembles/{block_type}/"
        f"gerry_toward_{party}_using_{election}_data/"
        f"init_part_{init_part}_random_seed_{random_seed}_burst_length_{burst_length}_{total_steps}_steps_assignment.ben"
    )
    save_updaters_results_to = (
        f"{CURRENT_WORKING_DIRECTORY}/MT_results_(replicated)/gerry/gerry_updaters/{block_type}/"
        f"gerry_toward_{party}_using_{election}_data/"
        f"init_part_{init_part}_random_seed_{random_seed}_burst_length_{burst_length}_{total_steps}_steps_updaters.jsonl"
    )
    os.makedirs(os.path.dirname(save_assignment_results_to), exist_ok=True)
    os.makedirs(os.path.dirname(save_updaters_results_to), exist_ok=True)

    # Set pop data, random seed
    pop_col = "total_pop"
    random.seed(random_seed)

    # Define updaters.
    # We define different updaters depending on what election data we're using to determine winners
    # because we're only using those columns to implement our optimization function.
    if election == "pres":
        my_updaters = {
            "population": updaters.Tally(pop_col, alias="population"),
            "pres_election": Election(
                "pres_election", {"D": "PRES20DEM", "R": "PRES20REP"}
            ),
            "sen_election": Election(
                "sen_election", {"D": "SEN20DEM", "R": "SEN20REP"}
            ),
            "D_vote_population": updaters.Tally("PRES20DEM", alias="D_vote_population"),
            "R_vote_population": updaters.Tally("PRES20REP", alias="R_vote_population"),
            "total_vote_population": updaters.Tally(
                ["PRES20DEM", "PRES20REP"], alias="total_vote_population"
            ),
        }

    elif election == "sen":
        my_updaters = {
            "population": updaters.Tally(pop_col, alias="population"),
            "pres_election": Election(
                "pres_election", {"D": "PRES20DEM", "R": "PRES20REP"}
            ),
            "sen_election": Election(
                "sen_election", {"D": "SEN20DEM", "R": "SEN20REP"}
            ),
            "D_vote_population": updaters.Tally("SEN20DEM", alias="D_vote_population"),
            "R_vote_population": updaters.Tally("SEN20REP", alias="R_vote_population"),
            "total_vote_population": updaters.Tally(
                ["SEN20DEM", "SEN20REP"], alias="total_vote_population"
            ),
        }

    # For implementation of Gingleator, take "minority group" to be whichever party we're gerrymandering toward
    minority_pop_col = f"{party}_vote_population"

    # Set initial partition
    initial_partition = Partition(
        dual_graph,
        assignment=f"init_part_{init_part}",
        updaters=my_updaters
    )

    # Set ReCom chain
    # Note: total population is 1,084,225, hence rounded population target for 50 districts is 21,685
    proposal = partial(
        recom,
        pop_col=pop_col,
        pop_target=21685,
        epsilon=0.05,
        node_repeats=2,
        method=partial(bipartition_tree, allow_pair_reselection=True),
    )

    recom_chain = Gingleator(
        proposal=proposal,
        constraints=[contiguous],
        threshold=0.5,
        initial_state=initial_partition,
        total_pop_col="total_vote_population",
        minority_pop_col=minority_pop_col,
        score_function=safe_reward_partial_dist,
    )

    # Save results
    with (
        PyBenEncoder(save_assignment_results_to, overwrite=True) as encoder,
        jl.open(save_updaters_results_to, "w") as updater_output_file
    ):
        for i, plan in enumerate(recom_chain.short_bursts(burst_length, round(total_steps / burst_length))):

            # Save assignments
            assignment_series = plan.assignment.to_series()
            ordered_assignment = (
                assignment_series.loc[graph_node_order].astype(int).tolist()
            )
            encoder.write(ordered_assignment)

            if i % 100 == 0:
                print(f"Processing plan {i}...")

            assert (
                plan is not None
            ), "Something went terribly wrong. There is no output partition."

            # Save updaters
            pres_election = plan["pres_election"]
            sen_election = plan["sen_election"]

            pres_seats_won = {
                "D": pres_election.seats("D"),
                "R": pres_election.seats("R"),
            }

            sen_seats_won = {
                "D": sen_election.seats("D"),
                "R": sen_election.seats("R"),
            }

            pres_regions = pres_election.regions
            sen_regions = sen_election.regions

            pres_d_counts = pres_election.counts("D")
            pres_r_counts = pres_election.counts("R")
            pres_d_votes_by_district = dict(zip(pres_regions, pres_d_counts))
            pres_r_votes_by_district = dict(zip(pres_regions, pres_r_counts))

            sen_d_counts = sen_election.counts("D")
            sen_r_counts = sen_election.counts("R")
            sen_d_votes_by_district = dict(zip(sen_regions, sen_d_counts))
            sen_r_votes_by_district = dict(zip(sen_regions, sen_r_counts))

            record = {
                "sample": i + 1,
                "population": dict(plan["population"]),
                "Pres seats won": pres_seats_won,
                "Pres D votes": pres_d_votes_by_district,
                "Pres R votes": pres_r_votes_by_district,
                "Sen seats won": sen_seats_won,
                "Sen D votes": sen_d_votes_by_district,
                "Sen R votes": sen_r_votes_by_district
            }

            updater_output_file.write(record)