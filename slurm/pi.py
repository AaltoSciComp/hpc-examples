#!/usr/bin/env python3
from __future__ import division, print_function
from multiprocessing import Pool
import argparse
import random
import json
import sys
import time

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

def estimate_pi(iterations, seed, threads=1, serial=0.0):
    print("Calculating Pi via %d stochastic trials" % iterations,
            file=sys.stderr)

    if threads > 1:
        # Compute how much will be done in each worker.
        iterations_serial = int(serial*iterations)
        iterations_parallel = iterations - iterations_serial
        iterations_per_worker = iterations_parallel//threads
        print("Using %d threads (%d iterations each)" % \
                (threads, iterations_per_worker), file=sys.stderr)
        if serial > 0:
            print("... and %d iterations in serial"%iterations_serial)

        # Basic setup and accumulators
        in_circle_points = 0
        iters_actual = 0
        random_gen = random.Random(seed)

        # Parallel part
        # Starts <threads> worker processes
        if serial > 0:
            print("Beginning parallel part")
        pool = Pool(processes=threads)
        seeds = [random_gen.randint(0, 2**32 - 1) for _ in range(threads)]
        iters_per_worker = [iterations_per_worker]*threads
        iters_actual += sum(iters_per_worker)
        # This is the actual calculation:
        in_circle_points =+ sum(pool.map(pic_wrapper, zip(iters_per_worker, seeds)))
        pool.close()

        # Serial part
        if serial > 0:
            print("Beginning serial part")
        iters_actual += iterations_serial
        # This is the actual calculation:
        in_circle_points += pic_wrapper((iterations_serial, random_gen.randint(0, 2**32 - 1)))

        # Returns Pi and in-circle points (successes)
        return in_circle_points*4/iters_actual, in_circle_points
    else:
        in_circle_points = points_in_circle(iterations, seed)
        return in_circle_points*4/iterations, in_circle_points

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--threads', type=int, help="Number of threads, "
            "using multiprocessing", default=1)
    parser.add_argument('--seed', type=int, help="Random seed", default=42)
    parser.add_argument('--sleep', type=int, help="Sleep this many seconds")
    parser.add_argument('--serial', type=float, default=0.0,
                        help="This fraction [0.0--1.0] of iterations to be run serial.")
    parser.add_argument('iters', type=int, help="Number of iterations")
    args = parser.parse_args()

    if args.serial < 0.0 or args.serial > 1.0:
        print("ERROR: --serial should be a fraction from 0.0 to 1.0 (not percent).  (given: %s)"%args.serial)
        sys.exit(1)


    # Calculate Pi and number of in-circle points (successes)
    pi, successes = estimate_pi(args.iters, args.seed, args.threads, serial=args.serial)
    # Sleep
    if args.sleep:
        time.sleep(args.sleep)

    # Write to a JSON file
    result = {"pi_estimate":pi, "iterations":args.iters, "successes":successes}
    json.dump(result, sys.stdout)
    sys.stdout.write('\n')
