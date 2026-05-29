from add_init_parts_to_blocks_6 import add_init_parts_6
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
    add_init_parts_6(block_size)

if __name__ == "__main__":
    main()