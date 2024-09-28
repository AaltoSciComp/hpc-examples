#!/usr/bin/env python
import os
from time import time
import psutil

import numpy as np

print('Using %d processors' % int(os.getenv('SLURM_CPUS_PER_TASK') or '1'))
print('Using %d threads' % int(os.getenv('OMP_NUM_THREADS') or psutil.cpu_count()))
print('Using %d tasks' % int(os.getenv('SLURM_NTASKS') or '1'))

nrounds = 5

t_start = time()

for i in range(nrounds):
    a = np.random.random([2000,2000])
    a = a + a.T
    b = np.linalg.pinv(a)

t_delta = time() - t_start

print('Seconds taken to invert %d symmetric 2000x2000 matrices: %f' % (nrounds, t_delta))
