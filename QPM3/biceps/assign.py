import numpy as np
import mdtraj as md
import os, sys
if not os.path.exists('state'):
	os.mkdir('state')

a=np.load('assignments.npy')[0] # Assignment file
b=dict()
for j in range(20):	# number of states
	b[j]=[]
	for i in range(len(a)):
		if a[i]==j:
			b[j].append(i)
	np.save('state/state%d.npy'%j,b[j])
