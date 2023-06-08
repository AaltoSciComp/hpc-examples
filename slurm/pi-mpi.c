#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
  // MPI init
  int size, rank, hostname_len;
  char hostname[MPI_MAX_PROCESSOR_NAME];
  MPI_Init(NULL, NULL);
  MPI_Comm_size(MPI_COMM_WORLD, &size);
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  MPI_Get_processor_name(hostname, &hostname_len);
  // pi init
  long N=10000000;
  if (argc > 1)
    sscanf(argv[1], "%ld", &N);
  if (rank == 0)
    printf("Calculating pi using %ld stochastic trials\n", N);
  long N_rank = N / size;
  printf("%s: This is rank %d doing %ld trials\n", hostname, rank, N_rank);

  // Seed
  unsigned int seed = 5;
  seed += rank*5000;

  // Calculate trials
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

  // Sum all trials
  MPI_Reduce(&rank_count, &count, 1, MPI_LONG, MPI_SUM, 0, MPI_COMM_WORLD);

  if (rank == 0) {
    // pi/4 = count/N
    pi = (double) count*4/N;
    printf("Throws: %ld / %ld Pi: %.8g\n", count, N, pi);
  }

  MPI_Finalize();
  return (0);
}
