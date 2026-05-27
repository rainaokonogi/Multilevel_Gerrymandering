#!/usr/bin/env bash

WORKING_DIRECTORY="$(pwd)"

echo "started"
for random_seed in {1..5}; do
    for init_part in {1..5}; do
        for election in "pres" "sen"; do
            for party in "D" "R"; do
                for block_type in "blockgroups" "vtds" "tracts"; do

                    echo "Running with block_type=$block_type, election=$election, party=$party, init_part=$init_part, and random_seed=$random_seed"
                    PYTHONHASHSEED=0 uv run ${WORKING_DIRECTORY}/REPLICATION_REPO/MT_files/experiment_files/MT_gerry_exp_cli.py --block-type $block_type --election $election --party $party --init-part $init_part --random-seed $random_seed --burst-length 20 --total-steps 1000000

                done
            done
        done
    done
done