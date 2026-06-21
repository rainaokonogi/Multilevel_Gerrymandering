from gerrychain import Partition, Graph, accept, MarkovChain, updaters, Election
from gerrychain.proposals import recom
from gerrychain.tree import bipartition_tree
from gerrychain.constraints import contiguous
from gerrychain.accept import always_accept
from functools import partial
import random
import jsonlines as jl
import os
from pyben import PyBenEncoder
import json
from pathlib import Path

CURRENT_WORKING_DIRECTORY = Path.cwd()

def MT_neutral_exp(block_type, init_part, random_seed, total_steps):
    """Runs one neutral search of Montana redistricting plans.

    Args:
        block_type (str): type of census unit being aggregated into districts (blockgroups, VTDs, or tracts).
        init_part (int): Number of initial partition into districts to use for Markov chain (1–5)
        random_seed (int): Random seed for reproducibility.
        total_steps (int): Total number of steps for the chain; must be divisible by the burst length.
    """

    # Load dual graph of census units
    dual_graph_info = (
        f"{CURRENT_WORKING_DIRECTORY}/"
        f"/MT_files/dual_graphs/"
        f"MT_{block_type}_dual_graph_pop_balance_.05.json"
    )
    dual_graph = Graph.from_json(dual_graph_info)

    # For use later when saving results
    graph_node_order = list(dual_graph.nodes)

    # Create files to store new results; shouldn't overwrite results already in folder
    save_assignment_results_to = (
        f"{CURRENT_WORKING_DIRECTORY}/REP_DATA_(replicated)/Montana_results/neutral/neutral_ensembles/{block_type}/"
        f"init_part_{init_part}_random_seed_{random_seed}_{total_steps}_steps_assignment.ben"
    )
    save_updaters_results_to = (
        f"{CURRENT_WORKING_DIRECTORY}/REP_DATA_(replicated)/Montana_results/neutral/neutral_updaters/{block_type}/"
        f"init_part_{init_part}_random_seed_{random_seed}_{total_steps}_steps_updaters.jsonl"
    )
    os.makedirs(os.path.dirname(save_assignment_results_to), exist_ok=True)
    os.makedirs(os.path.dirname(save_updaters_results_to), exist_ok=True)

    # Set pop data, random seed
    pop_col = "POP20"
    random.seed(random_seed)

    # Define updaters
    my_updaters = {
            "population": updaters.Tally(pop_col, alias="population"),
            "pres_election": Election(
                "pres_election", {"D": "PRES20DEM", "R": "PRES20REP"}
            ),
            "sen_election": Election(
                "sen_election", {"D": "SEN20DEM", "R": "SEN20REP"}
            )
    }

    # Set initial partition
    initial_partition = Partition(
        dual_graph,
        assignment=f"init_part_{init_part}",
        updaters=my_updaters
    )

    # Set ReCom chain
    # Note: total pop is 1,084,225, hence rounded pop target for 50 districts is 21,685
    proposal = partial(
        recom,
        pop_col=pop_col,
        pop_target=21685,
        epsilon=0.05,
        node_repeats=2,
        method=partial(bipartition_tree, allow_pair_reselection=True),
    )

    recom_chain = MarkovChain(
        proposal=proposal,
        constraints=[contiguous],
        initial_state=initial_partition,
        accept=always_accept,
        total_steps=total_steps
    )

    # Save results
    with (
        PyBenEncoder(save_assignment_results_to, overwrite=True) as encoder,
        jl.open(save_updaters_results_to, "w") as updater_output_file
    ):
        for i, plan in enumerate(recom_chain):

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