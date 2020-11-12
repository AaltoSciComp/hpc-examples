#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
  // MPI init
  int size, rank;
  MPI_Init(NULL, NULL);
  MPI_Comm_size(MPI_COMM_WORLD, &size);
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  // pi init
  long N=10000000;
  if (argc > 1)
    sscanf(argv[1], "%ld", &N);
  if (rank == 0)
    printf("Calculating pi using %ld stochastic trials\n", N);
  int N_rank = N / size;
  printf("This is rank %d doing %ld trials\n", rank, N_rank);

  // Seed
  unsigned int seed = 5;
  seed += rank*5000;

  double x, y;
  long i;
  long rank_count = 0;

  for (i=0; i<N_rank; i++) {
    x = (double) rand_r(&seed)/RAND_MAX;
    y = (double) rand_r(&seed)/RAND_MAX;
    if (x*x + y*y <= 1)
      rank_count++;
  }

  double pi;
  long count;
  MPI_Reduce(&rank_count, &count, 1, MPI_LONG, MPI_SUM, 0, MPI_COMM_WORLD);

  if (rank == 0) {
    // pi/4 = count/N
    pi = (double) count*4/N;
    printf("%g\n", pi);
  }

  MPI_Finalize();
  return (0);
}
