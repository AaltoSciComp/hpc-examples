from __future__ import print_function
import numpy as np
import os
from argparse import ArgumentParser
import sys

parser = ArgumentParser(description='Opens a datafile containing a data matrix and inverts it')

parser.add_argument('--input',metavar='inputfile',nargs=1, help='Input file', required=True)
parser.add_argument('--output',metavar='outputfile',nargs=1, help='Output file', required=True)

args = parser.parse_args()

inputfile = os.path.abspath(args.input[0])
outputfile = os.path.abspath(args.output[0])

print('Inverting {0}'.format(inputfile))

data = np.loadtxt(inputfile)
data_inv = np.linalg.inv(data)
print('Saving output to {0}'.format(outputfile))
np.savetxt(outputfile, data_inv)
