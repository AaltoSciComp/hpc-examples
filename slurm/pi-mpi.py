# By Radovan Bast at
# https://aaltoscicomp.github.io/python-for-scicomp/parallel/

import random
import time
from mpi4py import MPI


def sample(n):
    """Make n trials of points in the square.  Return (n, number_in_circle)

    This is our basic function.  By design, it returns everything it\
    needs to compute the final answer: both n (even though it is an input
    argument) and n_inside_circle.  To compute our final answer, all we
    have to do is sum up the n:s and the n_inside_circle:s and do our
    computation"""
    n_inside_circle = 0
    for i in range(n):
        x = random.random()
        y = random.random()
        if x ** 2 + y ** 2 < 1.0:
            n_inside_circle += 1
    return n, n_inside_circle


comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
hostname = MPI.Get_processor_name()

n = 10 ** 7

if size > 1:
    n_task = int(n / size)
else:
    n_task = n

t0 = time.perf_counter()
_, n_inside_circle = sample(n_task)
t = time.perf_counter() - t0

print(f"before gather: rank {rank}, hostname {hostname}, n_inside_circle: {n_inside_circle}")
n_inside_circle = comm.gather(n_inside_circle, root=0)
print(f"after gather: rank {rank}, hostname {hostname}, n_inside_circle: {n_inside_circle}")

if rank == 0:
    pi_estimate = 4.0 * sum(n_inside_circle) / n
    print(
        f"\nnumber of darts: {n}, estimate: {pi_estimate}, time spent: {t:.2} seconds"
    )
