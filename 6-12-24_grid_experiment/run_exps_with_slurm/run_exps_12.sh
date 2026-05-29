#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOP_DIR="$(realpath "${SCRIPT_DIR}/..")"

echo $TOP_DIR

echo "started"
for assort_score in "med"; do
    for random_seed in 3 4 5; do
        for init_part in 1 2 3; do
            for experiment_type in "NG"; do
                for map_number in 1; do
                    for num_r_units in 18 21; do
                        for block_size in 1 2 3; do
                            echo "Running with assort_score=$assort_score, num_r_units=$num_r_units, map_number=$map_number, block_size=$block_size, experiment_type=$experiment_type, init_part=$init_part, and random_seed=$random_seed"
                            sbatch --job-name="12-syn-exps" \
                                --nodes=1 \
                                --ntasks=1 \
                                --partition=duchin \
                                --cpus-per-task=2 \
                                --mem=2G \
                                --time=4-00:00:00 \
                                --error="12-error_files/syn_error_${assort_score}_r_${num_r_units}_map_${map_number}_block_size_${block_size}_${experiment_type}_init_part_${init_part}_seed_${random_seed}.log" \
                                --output="12-output_files/syn_output_${assort_score}_r_${num_r_units}_map_${map_number}_block_size_${block_size}_${experiment_type}_init_part_${init_part}_seed_${random_seed}.out" \
                                --wrap="PYTHONHASHSEED=0 uv run /share/duchin/raina/6-12-24_grid_exp/syn_exps_cli_12.py --assort-score $assort_score --num-r-units $num_r_units --map-number $map_number --block-size $block_size --experiment-type $experiment_type --init-part $init_part --random-seed $random_seed --burst-length 20 --total-steps 20000"
                        done
                    done
                done
            done
        done
    done
done