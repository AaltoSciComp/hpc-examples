"""Combine counts files

Reads in multiple files and writes out a new count file.

"""

import argparse
import collections
import json
import sys

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('countfile', nargs='+', help="Files with counts")
parser.add_argument('--verbose', '-v', action='store_true')
parser.add_argument('--output', '-o',)
args = parser.parse_args()

ngrams_total = collections.Counter()
for file_ in args.countfile:
    if args.verbose:
        print(file_, file=sys.stderr)
    for line in open(file_):
        if not line.strip():
            continue
        count, data = line.split(' ', 1)
        count = int(count)
        data = json.loads(data)
        ngrams_total[tuple(data)] += count

# Save output to file if requested, otherwise print to stdout
output = sys.stdout
if args.output:
    if args.verbose:
        print('Writing to', args.output, file=sys.stderr)
    output = open(args.output, 'w')
# Print the output
for ngram, count in ngrams_total.most_common():
    print(count, json.dumps(ngram), file=output)
