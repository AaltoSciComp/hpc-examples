#!/usr/bin/env python3
"""Aggregation script for Pi estimations

This script aggregates the results produced
by running ``pi.py``. The output is in the same
format as that of ``pi.py``.

Example:
    If results of ``pi.py`` are ouput to files ``result1.json``,
    ``result2.json``, etc. then you can calculate weighted
    average of the estimates by::

       $ python pi_aggregation.py result1.json result2.json ...

    The result would be a more accurate estimation of Pi.

"""

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
