#!/usr/bin/env python
#SBATCH -p interactive
#SBATCH -t 00:5:00

from __future__ import print_function

import os
print(os.environ)

# If you have an array job, you can access it this way:
print(os.environ['SLURM_ARRAY_TASK_ID'])
