"""Count ngrams from input text files (multiprocessing version).

This reads in text files and computes n-grams based on words or
characters.  It's designed to be a HPC example, not for serious use.

The multiprocessing version is slower than the non-multiprocessing
version (this is something for you to think about).

n-grams are tuples such as ("the", "book", "is") or ("t", "h", "e").  It
writes output to standard output, or the file given.  Output format a
plain-text file with:

COUNT ["word1", "word2"]

"""
from __future__ import print_function

import collections
import io
import itertools
import json
import multiprocessing
import os
import re
import resource
import sys
import time
import zipfile



def nwise(iterable, n):
    """Like itertools.pairwise but for arbitrary n.

    Creates groups of n:

    1: [a, b, c, d, e, f] -> [a, b, c, d, e, f]
    2: [a, b, c, d, e, f] -> [ab, bc, cd, de, ef]
    3: [a, b, c, d, e, f] -> [abc, bcd, cde, def]
    """
    if n <= 0:
        raise ValueError(f"n must be a positive integer (was {n})")
    iterator = iter(iterable)
    try:
        ngram = tuple(next(iterator) for _ in range(n))
    # RuntimeError raised within the above when it runs out of data.
    # Does this mask other errors though?
    except RuntimeError:
        return
    yield ngram
    for next_ in iterator:
        ngram = ngram[1:] + (next_, )
        yield ngram

def _openzip(zip, name):
    return lambda: io.TextIOWrapper(z.open(name), 'utf8')

def opendir(dir_):
    """Open either a zipfile (*.txt within it), directory/*.txt, or an individual file.

    Returns a list of the files within the zipfile or directory, or the
    filename if a single filename is given.  The list contains
    (filename, function_that_opens_the _file), so that the process_file
    function can handle both zipfiles and normal files the same way.
    """
    # Zipfiles
    if dir_.endswith('.zip'):
        z = zipfile.ZipFile(dir_)
        file_list = [ #(z, name)
                      f'zip::{dir_}::{name}'
                      for name in z.namelist()
                      if name.endswith('.txt') ]
        print(f'Found {len(file_list)} files in {dir_}', file=sys.stderr)
    # Directories
    elif os.path.isdir(dir_):
        file_list = [ #(name, lambda name=name: open(name, 'r'))
                      os.path.join(dir_, name)
                      for name in os.listdir(dir_)
                      if name.endswith('.txt') ]
        print(f'Found {len(file_list)} files in {dir_}', file=sys.stderr)
    # regular files
    else:
        file_list = [ dir_ ]
    return file_list

ZIPFILE_CACHE = { }
def process_file(x):
    """Return ngrams from a given filename.

    filename: filename of this file.  Only used for printing, since it
    might be a relative path inside of a zipfile.

    data: a function which returns the file data.  This exists so that
    this function doesn't need to care if it's reading from a zipfile or
    normal file.

    args: arguments from the argument parser.
    """
    filename, args = x
    if args.verbose:
        print(filename, file=sys.stderr)
    # Open the zipfile and cache the open zipfile object.
    if filename.startswith('zip::'):
        _, archive, element = filename.split('::', maxsplit=2)
        if archive in ZIPFILE_CACHE:
            z = ZIPFILE_CACHE[archive]
        else:
            #z = zipfile.ZipFile(archive)
            z = ZIPFILE_CACHE[archive] = zipfile.ZipFile(archive)
        data = z.open(element).read().decode()
    #if isinstance(filename, tuple):
    #    name, data = filename
    #    if isinstance(name, zipfile.ZipFile):
    #        z, name = name, data
    #        data = z.open(name).read()
    #    #z = zipfile.ZipFile(archive)
    #    data = data.decode()
    else:
        data = open(filename, 'r').read()
    data = data.lower()
    ngrams = collections.Counter() # Making a new Counter here may be inefficient.
    # Split by words if needed.  Use a regular expression for this.
    if args.words:
        data = (m[0] for m in re.finditer(r'[a-zA-Z_-]+', data))
    # For every ngram, increment its count
    for ngram in nwise(data, args.n):
        ngrams[ngram] += 1

    return ngrams



def arg_int_auto(x):
    """Argparse argument type helper.

    Returns an integer, or the value from the environment variable
    SLURM_CPUS_PER_TASK if the value is 'auto'.
    """
    if x == 'auto':
        return int(os.environ['SLURM_CPUS_PER_TASK'])
    else:
        return int(x)



def main():
    start = time.time()
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs='+', help="Inputs, should be text files.  Can be a zipfile or directory (in which case, files ending in .txt inside the zip/directory will be used), or directly filenames (in which case the file will be used)")
    parser.add_argument('-n', type=int, default=1, help="Size of n-grams.  -n 1 is simple frequencies.")
    parser.add_argument('--output', '-o', help="Write output to this filename, otherwise print output to stdout.")
    parser.add_argument('--threads', '-t', type=arg_int_auto, default=1, help="Number of threads to usez for the analysis.  If 'auto', then detect from the SLURM_CPUS_PER_TASK environment variable.  If an integer 1 or greater, use multiprocessing with that many processes.  If zero, do not use multiprocessing at all.  Default: 1")
    parser.add_argument('--words', action='store_true', help="If given, use word-based ngram mode instead of character-based.  Word-based mode only uses ascii letters and removes most other punctuation and special characters.")
    parser.add_argument('--verbose', '-v', action='store_true', help="Print more to stderr, for example the filenames that are being read.")
    group_selection = parser.add_argument_group("selection", "Selecting files.  After a list of all files is created, apply these slice operations like you do to a list: list[start:stop:step].  Files are not sorted and used in the order given, order in the zipfile, or order the natural (unsorted) order the operating system returns them from the directory list.  The directory order is unpredictable but usually the same if the directory isn't touched.")
    group_selection.add_argument('--start', type=int, default=None, help="Select starting file with a Python slice operation 'file_list[start:]'.  The start is included, and counts go from 0.  For examaple, --start=1 skips the first (0th) file.")
    group_selection.add_argument('--stop', type=int, default=None, help="Select stop file with file_list[:stop].  The stop is NOT included, and the counts go from zero.  For example, to limit to the first 100 files (0, 1, ..., 99), use --stop=100 .")
    group_selection.add_argument('--step', type=int, default=None, help="Select every STEP file.  For example, --start=0 --step=10 selects files 0, 10, 20, etc. and --start=1 --step=10 selects files 1, 11, 21, etc.")
    args = parser.parse_args()

    # Read the filelist from a zipfile, OR from a directory.  Accumulate
    # a list of all files across all arguments.
    filelist = sum((opendir(input) for input in args.input), [])
    filelist = itertools.islice(filelist, args.start, args.stop, args.step)

    # Process every file and accumulate the counts.
    ngrams_total = collections.Counter()
    if args.threads is not None and args.threads != 0:
        print(f'Using multiprocessing.Pool with {args.threads} processes', file=sys.stderr)
        pool = multiprocessing.Pool(args.threads)
        for result in pool.imap_unordered(process_file,
                                          (
                                           (name, args)
                                           #((name[1], name[0].open(name[1]).read()), args) if isinstance(name, tuple) else (name, args)
                                           for name in filelist),
                                           chunksize=10,
                                         ):
            ngrams_total.update(result)
        pool.close()
        pool.join()
    else:
        for filename in filelist:
            ngrams_total.update(process_file((filename, args)))

    # Save output to file if requested, otherwise print to stdout
    output = sys.stdout
    if args.output:
        output = open(args.output, 'w')
    for ngram, count in ngrams_total.most_common():
        print(count, json.dumps(ngram), file=output)

    # Print the summary and performance information to stderr
    print(f'{args.n}-grams: {len(ngrams_total)}', file=sys.stderr)
    print(file=sys.stderr)
    rusage_s = resource.getrusage(resource.RUSAGE_SELF)
    rusage_c = resource.getrusage(resource.RUSAGE_CHILDREN)
    print(f'Walltime {time.time() - start:.2f} s', file=sys.stderr)
    print(f'User time: {rusage_s.ru_utime + rusage_c.ru_utime:.2f} s ({rusage_s.ru_utime:.2f} + {rusage_c.ru_utime:.2f})', file=sys.stderr)
    print(f'System time: {rusage_s.ru_stime + rusage_c.ru_stime:.2f} s ({rusage_s.ru_stime:.2f} + {rusage_c.ru_stime:.2f})', file=sys.stderr)
    print(f'MaxRSS: {(rusage_s.ru_maxrss + rusage_c.ru_maxrss)/2**20:.3f} GiB ({rusage_s.ru_maxrss/2**20:.3f} + {rusage_c.ru_maxrss/2**20:.3f})', file=sys.stderr)

if __name__ == '__main__':
    main()
