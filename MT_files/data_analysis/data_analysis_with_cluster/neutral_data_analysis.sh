#!/bin/bash
#SBATCH --job-name=MT-neutral-analysis
#SBATCH --array=0-1
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=4G
#SBATCH --time=2-00:00:00
#SBATCH --output=logs/MT_neutral_analysis_output_%A_%a.out
#SBATCH --error=logs/MT_neutral_analysis_error_%A_%a.log

WORKING_DIRECTORY="$(pwd)"

scripts=(
    "collect_pres_histogram_data_from_neutral_results.py" 
    "collect_sen_histogram_data_from_neutral_results.py"
)

python3 "${WORKING_DIRECTORY}/MT_files/data_analysis/${scripts[$SLURM_ARRAY_TASK_ID]}"