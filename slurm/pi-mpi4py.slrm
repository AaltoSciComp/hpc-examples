#!/bin/bash
#SBATCH --time=00:10:00
#SBATCH --mem=2G
#SBATCH --output=pi-mpi4py.out
#SBATCH --ntasks=4

module purge
module load anaconda

mpirun python pi-mpi.py
