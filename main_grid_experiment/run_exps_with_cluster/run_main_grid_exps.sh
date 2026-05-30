#!/usr/bin/env bash

WORKING_DIRECTORY="$(pwd)"

echo $TOP_DIR

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
                                sbatch --job-name="syn-exps" \
                                    --nodes=1 \
                                    --ntasks=1 \
                                    --partition=duchin \
                                    --cpus-per-task=2 \
                                    --mem=2G \
                                    --time=4-00:00:00 \
                                    --error="syn_error_files/syn_error_assort_score_${assort_score}_r_${num_r_units}_map_${map_number}_block_size_${block_size}_${experiment_type}_init_part_${init_part}_seed_${random_seed}_party_${party}.log" \
                                    --output="syn_output_files/syn_output_${assort_score}_r_${num_r_units}_map_${map_number}_block_size_${block_size}_${experiment_type}_init_part_${init_part}_seed_${random_seed}_party_${party}.out" \
                                    --wrap="PYTHONHASHSEED=0 uv run ${WORKING_DIRECTORY}/syn_files/syn_exps_cli.py --assort-score $assort_score --num-r-units $num_r_units --map-number $map_number --block-size $block_size --experiment-type $experiment_type --init-part $init_part --random-seed $random_seed --party $party --burst-length 20 --total-steps 20000"
                            done
                        done
                    done
                done
            done
        done
    done
done