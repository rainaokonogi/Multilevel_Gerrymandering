from make_6_block_partitions import make_6_blocks
import click

@click.command()

@click.option(
    "--block-size",
    prompt="",
    help="",
    type=int,
)

def main(
    block_size
):
    make_6_blocks(block_size)

if __name__ == "__main__":
    main()