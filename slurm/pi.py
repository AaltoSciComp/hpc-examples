#!/usr/bin/env python3
from __future__ import division, print_function
from multiprocessing import Pool
import argparse
import random
import sys

def is_in_circle(gen):
    x = gen.uniform(0, 1)
    y = gen.uniform(0, 1) 
    return x**2 + y**2 < 1

def points_in_circle(iterations, seed):
    gen = random.Random(seed)
    return sum(1 for _ in range(iterations) if is_in_circle(gen))

# python2 does not come with Pool.starmap...
def pic_wrapper(a):
    return points_in_circle(*a)

def estimate_pi(iterations, seed, threads=1):
    print("Calculating Pi via %d stochastic trials" % iterations,
            file=sys.stderr)

    if threads > 1:
        iterations_per_worker = iterations//threads
        print("Using %d threads (%d iterations each)" % \
                (threads, iterations_per_worker), file=sys.stderr)

        # Starts <threads> worker processes
        pool = Pool(processes=threads)

        gen = random.Random(seed)
        seeds = [gen.randint(0, 2**32-1) for _ in range(threads)]
        iters = [iterations_per_worker]*threads
        in_circle_points = pool.map(pic_wrapper, zip(iters, seeds))

        pool.close()

        # Total number of in-circle points
        return sum(in_circle_points)*4/sum(iters)
    else:
        return points_in_circle(iterations, seed)*4/iterations

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--threads', type=int, help="Number of threads, "
            "using multiprocessing", default=1)
    parser.add_argument('--seed', type=int, help="Random seed", default=42)
    parser.add_argument('iters', type=int, help="Number of iterations")
    args = parser.parse_args()
    pi = estimate_pi(args.iters, args.seed, args.threads)
    print("Pi =", pi)
