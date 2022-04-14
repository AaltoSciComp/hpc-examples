#!/bin/bash
#
# Build a postgres image using singularity
#

export SINGULARITY_CACHEDIR=/tmp/$USER/singularity_cache
mkdir -p $SINGULARITY_CACHEDIR

singularity pull docker://library/postgres:latest
