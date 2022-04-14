#!/bin/bash
#SBATCH --output=postgres_example.out
#SBATCH --time=00:30:00
#SBATCH --mem=2G

# Quit if any errors occur

set -e

# Create directories for postgresql to store data

mkdir -p var/{lib,run}

# Run postgres in a singularity image, forward output to files, catch PID for process

singularity run --env POSTGRES_PASSWORD=mysecretpassword --env LC_ALL=C -B ${PWD}/var/lib:/var/lib/postgresql -B ${PWD}/var/run:/var/run postgres_latest.sif 2> postgres.err 1> postgres.out &
POSTGRES_PID=$!

# Give postgres few seconds to initialize

sleep 5

# Set up a trap so that postgres will be killed when job finishes

trap "kill $POSTGRES_PID ; exit" TERM EXIT

# Create test environment

module load miniconda

mamba create -n sqlalchemy_test -q -y python sqlalchemy psycopg2

source activate sqlalchemy_test

# Run test connection to postgresql

echo 'Testing postgres writing:'

python test_postgres_write.py

echo 'Testing postgres reading:'

python test_postgres_read.py

# Remove test environment

source deactivate

mamba env remove -n sqlalchemy_test
