#!/bin/bash
#SBATCH --time=00:05:00
#SBATCH --job-name=helloworld
#SBATCH --mem-per-cpu=500M
#SBATCH --cpus-per-task=1
#SBATCH --gres=gpu:1
#SBATCH --output=helloworld.out

module load cuda
nvcc helloworld.cu -o helloworld
./helloworld
