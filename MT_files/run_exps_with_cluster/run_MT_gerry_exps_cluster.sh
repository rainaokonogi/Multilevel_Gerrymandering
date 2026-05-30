#!/usr/bin/env bash

WORKING_DIRECTORY="$(pwd)"

echo "started"
for random_seed in {1..5}; do
    for init_part in {1..5}; do
        for election in "pres" "sen"; do
            for party in "D" "R"; do
                for block_type in "vtds" "blockgroups" "tracts"; do

                    echo "Running with block_type=$block_type, election=$election, party=$party, init_part=$init_part, and random_seed=$random_seed"
                    
                    sbatch --job-name="MT-${block_type}-${election}-${party}--part-${init_part}-seed-${random_seed}" \
                        --nodes=1 \
                        --ntasks=1 \
                        --cpus-per-task=2 \
                        --mem=2G \
                        --time=4-00:00:00 \
                        --error="MT_gerry_error_files/MT_gerry_exps_${block_type}_${election}_${party}_part_${init_part}_seed_${random_seed}.log" \
                        --output="MT_gerry_output_files/MT_gerry_exps_${block_type}_${election}_${party}_part_${init_part}_seed_${random_seed}.out" \
                        --wrap="PYTHONHASHSEED=0 uv run ${WORKING_DIRECTORY}/MT_files/experiment_files/MT_gerry_exp_cli.py --block-type $block_type --election $election --party $party --init-part $init_part --random-seed $random_seed --burst-length 20 --total-steps 1000000"
                        
                done
            done
        done
    done
done