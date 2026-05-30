#!/bin/bash
#SBATCH --job-name=MT-gerry-analysis
#SBATCH --array=0-3
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=4G
#SBATCH --time=2-00:00:00
#SBATCH --output=logs/MT_gerry_analysis_output_%A_%a.out
#SBATCH --error=logs/MT_gerry_analysis_error_%A_%a.log

WORKING_DIRECTORY="$(pwd)"

scripts=(
    "compute_pres_maximums_from_gerry_results.py"
    "compute_pres_minimums_from_gerry_results.py"
    "compute_sen_maximums_from_gerry_results.py"
    "compute_sen_minimums_from_gerry_results.py"
)

python3 "${WORKING_DIRECTORY}/MT_files/data_analysis/${scripts[$SLURM_ARRAY_TASK_ID]}"