# openmp/hello_omp

For up to date instructions, see
[SciComp page on parallel computing](https://scicomp.aalto.fi/triton/tut/parallel/).

Compiling the example with OpenMP:
```sh
module load gcc/9.2.0
gcc -fopenmp -O2 -g hello_omp.c -o hello_omp
```

Compiling the example without OpenMP:
```sh
module load gcc/9.2.0
gcc -O2 -g hello_omp.c -o hello_omp
```

Running the example in the queue:
```sh
sbatch hello_omp.slrm
```
or
```sh
module load gcc/9.2.0
export OMP_PROC_BIND=true
srun -c 2 ./hello_omp
```
