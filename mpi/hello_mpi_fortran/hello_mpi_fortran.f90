! Hello World MPI
!
! Compile on Triton with:
!
! module load gcc
! module load openmpi
! mpifort hello_mpi_fortran.f90 -o hello_mpi_fortran
! 
!
! Simo Tuomisto, 2021
!

program hello
   include 'mpif.h'
   integer world_size, rank, ierror, tag, status(MPI_STATUS_SIZE)
   
   call MPI_INIT(ierror) ! Initialize the MPI
   call MPI_COMM_SIZE(MPI_COMM_WORLD, world_size, ierror) ! Number of processes
   call MPI_COMM_RANK(MPI_COMM_WORLD, rank, ierror) ! Rank of the process
   print *, 'Hello world from processor ', rank, ' out of ', &
         world_size , ' processors'
   call MPI_FINALIZE(ierror) ! Finalize the MPI
   end
