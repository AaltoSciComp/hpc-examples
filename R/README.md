# R in Triton

These examples describe how to run R in the Triton cluster

## R serial example

This example runs a simple R script that trains a Caret model.

Usage:
```bash
sbatch serialR.slrm
```

## R parallel example

This example runs a non-vectorized code in serial and parallel for 1 to 4 cpus.

Code is adapted from an excellent blog post in http://www.parallelr.com/r-with-parallel-computing/ . Code is based on the ExplicitParallel.R example in https://github.com/PatricZhao/ParallelR/blob/master/PP_for_COS/ExplicitParallel.R .

Usage:
```bash
sbatch serialR.slrm
```
