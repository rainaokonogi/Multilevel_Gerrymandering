import click
from MT_neutral_exp import MT_neutral_exp

@click.command()

@click.option(
    "--block-type",
    prompt="Which census unit?",
    help="Type \"blockgroups\" \"vtds\", \"tracts\" or \"blocks\"",
    type=click.Choice(["blockgroups", "vtds", "tracts", "blocks"]),
)

@click.option(
    "--init-part",
    prompt="Which initial partition?",
    help="Options are 1, 2, 3, 4, or 5",
    type=click.Choice([1,2,3,4,5])
)

@click.option(
    "--random-seed",
    prompt="Random seed?",
    help="Give an integer to set the random seed",
    type=int
)

@click.option(
    "--total-steps",
    prompt="Number of steps in Markov chain? (Must be divisible by burst length)",
    help="Number of redistricting plans in one search",
    type=int
)

def main(
    block_type, init_part, random_seed, total_steps
):
    MT_neutral_exp(block_type, init_part, random_seed, total_steps)


if __name__ == "__main__":
    main()