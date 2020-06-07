/* Hello World MPI
 *
 * Compile on Triton as:
 *   module load openmpi
 *   mpicc -o hello_mpi.c hello_openmpi
 * 
 * degtyai1, Wed, 28 May 2014 12:47:47 +0300
 */

#include <mpi.h>
#include <stdio.h>

int main(int argc, char** argv) {
  MPI_Init(NULL, NULL); // initialize the MPI
  int world_size;
  MPI_Comm_size(MPI_COMM_WORLD, &world_size);  // number of processes
  int world_rank;
  MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);  // rank of the process
  char processor_name[MPI_MAX_PROCESSOR_NAME];
  int name_len;
  MPI_Get_processor_name(processor_name, &name_len); // processor name
  printf("Hello world from processor %s, rank %d"
   " out of %d processors\n", processor_name, world_rank, world_size);
  MPI_Finalize();   // finalize the MPI
}
