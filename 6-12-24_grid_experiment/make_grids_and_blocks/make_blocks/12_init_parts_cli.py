from add_init_parts_to_blocks_12 import add_init_parts_12
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
    add_init_parts_12(block_size)

if __name__ == "__main__":
    main()