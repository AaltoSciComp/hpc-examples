Python multiprocessing
======================


With Python multiprocessing pools, you have to set the number of CPUs that
the multiprcoessing pool, otherwise it will try to use every CPU on
the node - even though you haven't requested every CPU.  It will
be constricted to a few processors, but try to use them all.  This
will be inefficient.

The main point is to use the Slurm ``SLURM_CPUS_PER_TASK`` environment
variable to set the number of processors.


The Python file:

.. include::

   python_multiprocessing.py


.. include::

   python_multiprocessing.slrm
