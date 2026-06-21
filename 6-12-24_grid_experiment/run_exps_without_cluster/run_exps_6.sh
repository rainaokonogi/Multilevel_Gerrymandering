#!/usr/bin/env bash

WORKING_DIRECTORY="$(pwd)"

echo "started"
    for random_seed in {1..5}; do
        for init_part in {1..3}; do
            for experiment_type in "NN" "NG"; do
                for num_r_units in 18 21; do
                    for block_size in 1 2 3; do
                        for party in "D" "R"; do
                            echo "Running with num_r_units=$num_r_units, block_size=$block_size, experiment_type=$experiment_type, init_part=$init_part, random_seed=$random_seed, and party=$party"
                            PYTHONHASHSEED=0 uv run ${WORKING_DIRECTORY}/REPLICATION_REPO/6-12-24_grid_experiment/experiment_files/syn_exps_cli_6.py --num-r-units $num_r_units --block-size $block_size --experiment-type $experiment_type --init-part $init_part --random-seed $random_seed --burst-length 20 --total-steps 20000
                        done
                    done
                done
            done
        done
    done
done