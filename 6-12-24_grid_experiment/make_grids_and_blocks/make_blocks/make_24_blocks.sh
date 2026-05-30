#!/bin/bash 

echo "started"
for block_size in 2; do
    sbatch --job-name="24-exp-${block_size}" \
        --nodes=1 \
        --ntasks=1 \
        --partition=duchin \
        --cpus-per-task=2 \
        --mem=2G \
        --time=4-00:00:00 \
        --error="24-exp-${block_size}.log" \
        --output="24-exp-${block_size}.out" \
        --wrap="PYTHONHASHSEED=0 uv run /share/duchin/raina/6-12-24_grid_exp/block_size_24_cli.py --block-size $block_size"
done