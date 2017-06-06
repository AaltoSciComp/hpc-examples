# R in Triton

These examples describe how to run R in the Triton cluster

## R serial example

There are two examples. First runs a simple R script that trains a Caret model. Second runs the R-benchmark-25.R benchmark script.

Caret model is from Caret examples by Tobias Kind: https://github.com/tobigithub/caret-machine-learning/blob/master/caret-cv/caret-cv-simple.R

R-benchmark-25.R script from rbenchmarki repository: https://github.com/rbenchmark/benchmarks/tree/master/R-benchmark-25

Usage:
```bash
sbatch serialR.slrm
sbatch serialR.slrm
```

## R parallel example

This example runs a non-vectorized code in serial and parallel with 1 to 4 cpus.

Code is adapted from an excellent blog post in: http://www.parallelr.com/r-with-parallel-computing/ 

Raw code of the ExplicitParallel.R example is available in: https://github.com/PatricZhao/ParallelR/blob/master/PP_for_COS/ExplicitParallel.R

Usage:
```shell
sbatch parallelR.slrm
```

## R parallel example using Caret

This example runs a Caret training model in serial and parallel with 4 cpus.

Code is based on a Caret example by Tobias Kind: https://github.com/tobigithub/caret-machine-learning/wiki/caret-ml-parallel

Raw code is available in: https://github.com/tobigithub/caret-machine-learning/blob/master/caret-parallel/caret-parallel-train.R

Usage:
```shell
sbatch parallelR_Caret.slrm
```
