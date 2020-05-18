#!/usr/bin/env python3
from __future__ import print_function, division
import json
import sys

def calculate_average_pi(filenames):
    total_successes = 0
    total_iterations = 0
    for filename in filenames:
        with open(filename, 'r') as f:
            estimation = json.load(f)
            total_successes += estimation["successes"]
            total_iterations += estimation["iterations"]
    return total_successes, total_iterations

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("USAGE: {} file1.json file2.json ...".format(sys.argv[0]))
    successes, iterations = calculate_average_pi(sys.argv[1:])
    result = {"successes": successes, "iterations": iterations,
                "pi_estimate": successes*4/iterations}
    json.dump(result, sys.stdout)
