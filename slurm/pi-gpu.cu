#include "cuda_runtime.h"
#include "device_launch_parameters.h"
#include <curand.h>
#include <curand_kernel.h>
#include <stdint.h>
#include <stdio.h>

// Setup random number generator
__global__ void setup_rng(curandState *random_states,  uint64_t seed)
{
  int tid = threadIdx.x + blockIdx.x * blockDim.x;
  curand_init(seed, tid, 0, &random_states[tid]);
}

// Throw nthrows per thread
__global__ void throw_dart(curandState *random_states, int *nthrows, uint64_t *hits)
{
  int tid = threadIdx.x + blockIdx.x * blockDim.x;
  float random_x, random_y;
  curandState random_state = random_states[tid];

  hits[tid] = 0;
  for (int i=0; i<nthrows[tid]; i++) {
    random_x = curand_uniform(&random_state);
    random_y = curand_uniform(&random_state);

    if ((random_x*random_x + random_y*random_y) < 1.0) {
      hits[tid] += 1;
    }
  }
}

int main(int argc, char **argv) {

  // pi init
  long N=10000000;
  if (argc > 1)
    sscanf(argv[1], "%ld", &N);
  printf("Calculating pi using %ld stochastic trials\n", N);

  // Initialize variables
  int count, device;

  int *nthrows, *nthrows_gpu;
  uint64_t seed = 5;
  uint64_t *hits, *hits_gpu;
  curandState* random_states;
  uint64_t total_hits;
  float pi;

  // Run 2048 blocks
  int blocks = 512;
  // Run 128 threads per block.
  int threads = 128;

  int batch_size = blocks * threads;

  // Select device
  cudaGetDeviceCount(&count);
  cudaGetDevice(&device);

  // Allocate memory
  hits = (uint64_t*) malloc(batch_size*sizeof(uint64_t));
  nthrows = (int *) malloc(batch_size*sizeof(int));
  cudaMalloc(&hits_gpu, batch_size*sizeof(uint64_t));
  cudaMalloc(&nthrows_gpu, batch_size*sizeof(int));
  cudaMalloc(&random_states, batch_size*sizeof(curandState));

  // Calculate how many throws we want per thread
  for (int i=0; i<batch_size; i++) {
    nthrows[i] = N / batch_size;
    if (i < N % batch_size) {
      nthrows[i] += 1;
    }
  }

  // Copy throw number info to GPU VRAM
  cudaMemcpy(nthrows_gpu, nthrows, batch_size*sizeof(int), cudaMemcpyHostToDevice);

  // Initialize random number generator for each thread
  setup_rng<<<blocks, threads>>>(random_states, seed);

  // Throw darts
  throw_dart<<<blocks, threads>>>(random_states, nthrows_gpu, hits_gpu);

  // Copy hits to host RAM
  cudaMemcpy(hits, hits_gpu, batch_size*sizeof(uint64_t), cudaMemcpyDeviceToHost);

  // Calculate the total number of hits
  total_hits = 0;
  for (int i=0; i<batch_size; i++) {
    total_hits += hits[i];
  }

  // Calculate pi
  pi = (double) total_hits*4/N;
  printf("Throws: %lu/%lu Pi: %.10g\n", total_hits, N, pi);

  // Free memory
  free(hits);
  free(nthrows);
  cudaFree(hits_gpu);
  cudaFree(nthrows_gpu);
  cudaFree(random_states);

  return (0);
}
