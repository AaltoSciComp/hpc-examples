#!/bin/sh
#SBATCH --mem=1G
#SBATCH -c 1
#SBATCH --time=0:1:0
#SBATCH -J pi-calc
#SBATCH -o pi-out


#echo $SLURM_ARRAY_TASK_ID
srun python3 pi.py 1000000  #>> pi-out-$SLURM_ARRAY_TASK_ID
srun python3 pi.py 10000000 #>> pi-out-$SLURM_ARRAY_TASK_ID
