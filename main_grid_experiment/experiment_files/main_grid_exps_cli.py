import click
from NG import run_experiment_ng
from NN import run_experiment_nn

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
    type=click.Choice([72, 86]),
)
@click.option("--map-number",
    prompt="Which map to use? (1, 2, or 3)",
    help="",
    type=click.Choice([1, 2, 3])
)
@click.option("--block-size",
    prompt="Which block size? (1, 2, 3, 4, or 6)",
    help="",
    type=click.Choice([1, 2, 3, 4, 6])
)
@click.option("--experiment-type",
    prompt="Experiment type? (NN or NG)",
    help="",
    type=str
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
@click.option("--party",
    prompt="Gerrymandering towards? (D or R)",
    help="",
    type=str
)
@click.option(
    "--burst-length",
    type=int
)
@click.option(
    "--total-steps",
    prompt="Step count (must be divisible by burst length)",
    type=int,
    help="Number of districting plans per building block graph",
)
def main(
    assort_score, num_r_units, map_number, block_size, experiment_type, init_part, random_seed, party, burst_length, total_steps
):

    if experiment_type == "NG":
        run_experiment_ng(assort_score, num_r_units, map_number, block_size, init_part, random_seed, party, burst_length, total_steps)
    elif experiment_type == "NN":
        run_experiment_nn(assort_score, num_r_units, map_number, block_size, init_part, random_seed total_steps)

if __name__ == "__main__":
    main()