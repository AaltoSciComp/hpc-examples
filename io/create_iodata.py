#!/usr/binenv /python
from __future__ import print_function
import numpy as np
import os

ndata = 10
datadim = 200

datadir = os.path.join(os.getcwd(),'data')


print('Creating {0} {1}x{1} positive definite matrices.'.format(ndata,datadim))
for i in range(0,ndata):
	print('Creating dataset number %d' % i)
	datamatrix = np.random.rand(datadim,datadim)
	datamatrix = datamatrix + datamatrix.T
	np.savetxt(os.path.join(datadir,'inputmatrix_%04d.dat' % i),datamatrix)
print('Data created.')
