#!/usr/bin/env python3
from __future__ import print_function, division
import argparse
import random
from random import uniform
import sys

parser = argparse.ArgumentParser()
parser.add_argument('mem', help="Use this much memory")
args = parser.parse_args()


mem = args.mem
if mem.endswith('b'):            mem = int(mem[:-1])
elif mem.lower().endswith('k'):  mem = int(mem[:-1]) * 1000**1
elif mem.lower().endswith('m'):  mem = int(mem[:-1]) * 1000**2
elif mem.lower().endswith('g'):  mem = int(mem[:-1]) * 1000**3
elif mem.lower().endswith('t'):  mem = int(mem[:-1]) * 1000**4
else:                            mem = int(mem)

try:
    range = xrange
except NameError:
    pass

print("Trying to hog %d bytes of memory"%mem)

allocated = 1
array = [ bytearray(1) ]
import random
import gc
import resource
while True:
    allocated_next = allocated * 2
    array.append(bytearray(allocated_next-allocated))
    allocated = allocated_next
    gc.collect()
    actual_bytes = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024
    print("Using %d bytes so far (allocated: %s)"%(actual_bytes, allocated))
    if actual_bytes > mem:
        break

