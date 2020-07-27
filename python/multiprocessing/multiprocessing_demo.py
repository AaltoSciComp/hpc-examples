"""Demonstration of multiprocessing integrated with Slurm
"""

import multiprocessing
import os

# Detect the number of CPUs we have available.  If in slurm, use the SLURM_CPUS_PER_TASK environment variable which Slurm lets.
if 'SLURM_CPUS_PER_TASK' in os.environ:
    cpus = int(os.environ['SLURM_CPUS_PER_TASK'])
    print("Dectected %s CPUs through slurm"%cpus)
else:
    # None means that it will auto-detect based on os.cpu_count()
    cpus = None
    print("Running on default number of CPUs (default: all=%s)"%os.cpu_count())


def my_work(i):
    """This is a pointless function that uses a few CPUs-seconds.
    """
    print("Running thread %s"%i)
    for x in range(10000000):
        x ** 2
    return i

# Start the pool with the number of CPUs we found above, or default
# value.
with multiprocessing.Pool(cpus) as p:
    print(p.map(my_work, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))
