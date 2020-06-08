# python/python_openmp

For up to date instructions, see
[SciComp page on parallel computing](https://scicomp.aalto.fi/triton/tut/parallel/)
and
[SciComp page on Python](https://scicomp.aalto.fi/triton/apps/python/).


Running the example in the queue:
```sh
sbatch python_openmp.slrm
```
or
```sh
module load anaconda/2020-03-tf2
srun -c 2 --time=00:05:00 python python_openmp.py
```
