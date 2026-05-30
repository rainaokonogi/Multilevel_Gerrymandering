import click
from NN_24 import run_experiment_nn_24
from NG_24 import run_experiment_ng_24

# Add the choice type to everything.
@click.command()
@click.option(
    "--assort-score",
    prompt="Low, medium, or high?",
    help="",
    type=click.Choice(["low", "med", "high"]),
)
@click.option(
    "--num-r-units",
    prompt="Number of red units in underlying map",
    help="",
    type=int,
)
@click.option("--map-number",
    prompt="Which map to use? (1, 2, or 3)",
    help="",
    type=click.Choice([1, 2, 3])
)
@click.option("--block-size",
    prompt="Which block size? (1, 2, 3, 4, or 6)",
    help="",
    type=int
)
@click.option("--experiment-type",
    prompt="Experiment type? (GG, NG, GN, or NN)",
    help="",
    type=str
    # type=click.Choice(["GG", "GN", "NG", "NN","GGopp"])
)
@click.option(
    "--init-part",
    prompt="Number for initial partition",
    help="",
    type=click.Choice([1, 2, 3]),
)
@click.option(
    "--random-seed",
    prompt="Random seed",
    help="Integer to set random seed",
    type=int
)
@click.option(
    "--burst-length",
    prompt="Burst length for short bursts algorithm (should be 20)",
    type=int
)
@click.option(
    "--total-steps",
    prompt="Step count (must be divisible by 20)",
    type=int,
    help="Number of districting plans per building block graph",
)
def main(
    assort_score, num_r_units, map_number, block_size, experiment_type, init_part, random_seed, burst_length, total_steps
):
    if experiment_type == "NG":
        run_experiment_ng_24(assort_score, num_r_units, map_number, block_size, init_part, random_seed, burst_length, total_steps)
    elif experiment_type == "NN":
        run_experiment_nn_24(assort_score, num_r_units, map_number, block_size, init_part, random_seed, total_steps)

if __name__ == "__main__":
    main()