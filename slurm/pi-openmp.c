// Compile with -fopenmp
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
  long N=10000000, i;
  long count =0 ;
  //int chunk = 1000;
  double pi, x, y;

  unsigned int seed = 5;

  if (argc > 1)
    sscanf(argv[1], "%ld", &N);
  printf("Calculating pi using %ld stochastic trials\n", N);

  // Bug: does not seed per-thread.
#pragma omp parallel for private(i, x,y) firstprivate(seed) reduction(+:count)
  for (i=0; i<N; i++) {
    x = (double) rand_r(&seed)/RAND_MAX;
    y = (double) rand_r(&seed)/RAND_MAX;
    if (x*x + y*y <= 1)
      count++;
  }
  // pi/4 = count/N
  pi = (double) count*4/N;
  printf("%g\n", pi);

  return 0;
}
