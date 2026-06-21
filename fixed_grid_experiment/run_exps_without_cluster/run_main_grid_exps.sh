#!/usr/bin/env bash

WORKING_DIRECTORY="$(pwd)"

echo "started"
for assort_score in "low" "med" "high"; do
    for random_seed in {1..5}; do
        for init_part in {1..3}; do
            for experiment_type in "NN" "NG"; do
                for map_number in {1..3}; do
                    for num_r_units in 72 86; do
                        for block_size in 1 2 3 4 6; do
                            for party in "D" "R"; do
                                echo "Running with assort_score=$assort_score, num_r_units=$num_r_units, map_number=$map_number, block_size=$block_size, experiment_type=$experiment_type, init_part=$init_part, random_seed=$random_seed, and party=$party"
                                PYTHONHASHSEED=0 uv run ${WORKING_DIRECTORY}/fixed_grid_experiment/experiment_files/fixed_grid_exps_cli.py --assort-score $assort_score --num-r-units $num_r_units --map-number $map_number --block-size $block_size --experiment-type $experiment_type --init-part $init_part --random-seed $random_seed --party $party --burst-length 20 --total-steps 20000
                            done
                        done
                    done
                done
            done
        done
    done
done