import click
from NY_gerry_exp import NY_gerry_exp

@click.command()

@click.option(
    "--block-type",
    prompt="Which census unit?",
    help="Type \"blockgroups\" \"vtds\", or \"tracts\"",
    type=click.Choice(["blockgroups", "vtds", "tracts"]),
)

@click.option("--election",
    prompt="What election data are we using?",
    help="Type \"pres\" or \"sen\"",
    type=click.Choice(["pres","sen"]))

@click.option("--party",
    prompt="Gerrymandering toward which party?",
    help="Type \"D\" or \"R\"",
    type=click.Choice(["D","R"]))

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
    "--burst-length",
    prompt="Burst length?",
    help="Number of plans queried in one burst as implemented by short bursts optimization method",
    type=int
)

@click.option(
    "--total-steps",
    prompt="Number of steps in Markov chain? (Must be divisible by burst length)",
    help="Number of redistricting plans in one search",
    type=int
)

def main(
    block_type, election, party, init_part, random_seed, burst_length, total_steps
):
    NY_gerry_exp(block_type, election, party, init_part, random_seed, burst_length, total_steps)

if __name__ == "__main__":
    main()