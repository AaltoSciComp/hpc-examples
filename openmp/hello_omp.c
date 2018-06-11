/* Hello World OpenMP
 *
 * Compile on Triton as:
 *   gcc -fopenmp hello_omp.c -o hello_omp
 * 
 * degtyai1, Wed, 28 May 2014 12:47:47 +0300
 */


#include <stdio.h>
int main(void) {
  #pragma omp parallel
    printf("Hello, world.\n");
  return 0;
}
