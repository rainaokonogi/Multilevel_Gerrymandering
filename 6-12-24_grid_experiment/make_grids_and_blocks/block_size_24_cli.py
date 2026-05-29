from make_24_block_partitions import make_24_blocks
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
    make_24_blocks(block_size)

if __name__ == "__main__":
    main()