#!/usr/bin/env python3
from __future__ import print_function
import argparse
from time import sleep
import gc
import platform
import resource

if __name__ == "__main__":
      
    parser = argparse.ArgumentParser()
    parser.add_argument('mem', metavar="memory", 
            help="Use this much memory")
    parser.add_argument('--sleep', 
            help="Sleep this many seconds", type=int)
    args = parser.parse_args()

    # calculate the amount of memory requested in bytes
    mem = args.mem.lower()

    if mem.endswith('b'):
        mem = int(mem[:-1])

    elif mem.endswith('k'):
        mem = int(mem[:-1])*1000**1

    elif mem.endswith('m'):
        mem = int(mem[:-1])*1000**2

    elif mem.endswith('g'):
        mem = int(mem[:-1])*1000**3

    elif mem.endswith('t'):
        mem = int(mem[:-1])*1000**4
 
    else:
        mem = int(mem)

    print("Trying to hog %d bytes of memeory" %mem)

    allocated = 1
    array = [bytearray(1)]

    while True:
        array.append(bytearray(allocated))
        allocated *= 2
        gc.collect()
        actual_bytes = resource.getrusage(
                resource.RUSAGE_SELF).ru_maxrss*(1024 if \
                        platform.system() == 'Linux' else 1)
        print("Using %d bytes so far (allocated: %s)" 
                %(actual_bytes, allocated))
        if actual_bytes > mem:
            break

    if args.sleep:
        time = args.sleep
        sleep(time)
