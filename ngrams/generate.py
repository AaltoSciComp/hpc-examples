"""Use ngrams to create text.

This uses ngrams to predict next words.  It takes makes a mapping of
(the first (n-1) parts of the ngrams) to (the last element of the
ngram), and uses this to predict.  It's not very good but shows a minimal use.

"""

import ast
import argparse
import collections
import json
import random
import sys

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('countfile', nargs='+', help="Files with counts, as generated from count.py")
#parser.add_argument('--output', '-o',)
parser.add_argument('--words', action='store_true', help="Use 'words-mode' instead of character-mode.")
parser.add_argument('--count', '-c', type=int, default=100, help="Generate this many followups.")
parser.add_argument('--limit-in', type=int, help="Limit ", "Stop reading from the files in after this ngrams.")
parser.add_argument('--count-threshold', type=int, help="Don't read in ngrams with fewer than this many occurrances.  Used to ")
parser.add_argument('--verbose', '-v', action='count', default=0)
args = parser.parse_args()

ngrams = collections.defaultdict(collections.Counter)
for file_ in args.countfile:
    if args.verbose >= 1:
        print(f"Reading {file_}", file=sys.stderr)
    for line in open(file_):
        if not line.strip():
            continue
        count, data = line.split(' ', 1)
        count = int(count)
        if args.count_threshold and count < args.count_threshold:
            break
            continue
        data = json.loads(data)
        ngrams[tuple(data[:-1])][data[-1]] += count
        if args.limit_in and len(ngrams) > args.limit_in:
            break
    if args.limit_in and len(ngrams) > args.limit_in:
        break

# A random starting (n-1) gram.
start = random.choice(list(ngrams))
if args.words:
    print(' '.join(start), end=' ')
else:
    print(''.join(start), end='')


for i in range(args.count):
    if start not in ngrams:
        print()
        print(f"can not continue from {start}")
        break
    elif args.verbose >= 2:
        print(f"{start} has {len(ngrams_next)} possibilities", file=sys.stderr)
    ngrams_next = ngrams[start]
    next_ = random.choices(population=list(ngrams_next.keys()), weights=ngrams_next.values())
    next_ = next_[0]
    if args.words:
        print(next_, end=' ')
    else:
        print(next_, end='')
    start = start[1:] + (next_, )
print()
