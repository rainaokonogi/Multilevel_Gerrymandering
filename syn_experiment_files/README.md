To create the building blocks for this experiment, do the following:

First, run the following in the command line:
    PYTHONHASHSEED=0 uv run make_grid_maps.py.
This should instantly create the nine grid maps.

If using a cluster, then type the following into the command line:
1. bash make_building_blocks_files_cluster.sh (~4 hours)
2. bash add_init_parts_to_blocks_cluster.sh (~20–30 minutes)

If not using a cluster, instead type the following:
1. bash make_building_blocks_files.sh
2. bash add_init_parts_to_blocks.sh

After you have created or downloaded the building blocks, then run

If using cluster:
    run_syn_exps_cluster.sh

If not using cluster:
    run_syn_exps.sh


Note to self: need to resolve path issue here