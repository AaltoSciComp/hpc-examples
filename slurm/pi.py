from __future__ import print_function, division
from random import uniform
import sys

N = int(sys.argv[1])
print("Calculating pi via %i stochastic trials"%N)

def trial():
    return uniform(0,1)**2 + uniform(0,1)**2 < 1

successes = sum(1 for _ in range(N) if trial())

# pi/4 = successes/N
print(successes * 4 / N)
