#!/bin/bash
#SBATCH --mem=50G
#SBATCH --array=0-20
#SBATCH --time=0-6
#SBATCH --job-name=words-array

mkdir -p /scratch/work/$USER/ngrams-output/

python3 ngrams/count.py /scratch/work/darstr1/data/Gutenberg-Fiction.zip -n 3 --words --start=$SLURM_ARRAY_TASK_ID --step=20 -o /scratch/work/$USER/ngrams-output/ngrams3-words-all-array_$SLURM_ARRAY_TASK_ID.out

# Combine
#python3 ngrams/combine-counts.py /scratch/work/$USER/ngrams-output/ngrams3-words-all-array_* -o /scratch/work/$USER/ngrams-output/ngrams3-words-all.out
