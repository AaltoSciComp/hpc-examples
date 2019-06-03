#!/usr/bin/env python3
from __future__ import print_function, division
import argparse
import random
from random import uniform
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--threads', type=int, help="number of threads, using multiprocessing")
parser.add_argument('--seed', help="Random seed")
parser.add_argument('N', type=int, help="number of iterations total")
args = parser.parse_args()

N = args.N
if args.threads:
    # Ensure N is a multiple of threads
    N = (N//args.threads)*args.threads
    print("Using %d threads"%args.threads)
print("Calculating pi via %d stochastic trials"%N)
if args.seed:
    print("Setting random seed to %s"%args.seed)
    random.seed(args.seed)

def trial():
    return uniform(0,1)**2 + uniform(0,1)**2 < 1

def n_trials(n):
    successes = sum(1 for _ in range(n) if trial())
    return successes

if args.threads:
    from multiprocessing import Pool
    n = N // args.threads
    trials = [ n ] * args.threads
    pool = Pool(processes=args.threads)
    successes = pool.map(n_trials, trials)
    #print(successes)
    pool.close()
    successes = sum(successes)
else:
    successes = sum(1 for _ in range(N) if trial())

# pi/4 = successes/N
print("%d successes out of %d trials"%(successes, N))
print()
print("pi =", successes * 4 / N)
