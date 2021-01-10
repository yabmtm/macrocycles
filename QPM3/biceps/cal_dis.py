import numpy as np
import mdtraj as md
import os, sys
if not os.path.exists('NOE'):
	os.mkdir('NOE')

t=md.load('traj.xtc',top='xtc.gro')	# traj and top files
Ind=np.array([[17,45],[18,45],[69,97],[70,97],[121,149],[122,149],[153,15],[153,16],[49,67],[49,68],[101,119],[101,120],[153,14],[49,66],[101,118],[45,50],[97,102],[149,154]])	# Indices for distances (0 based!)

for i in range(20):	# number of states
        b=np.load('state/state%d.npy'%i) 
	if len(b) != 0:
		print i
	        p=[]
	        for z in b:
        	        d=md.compute_distances(t[z],Ind)
                	p.append(d)
	        u=[]
	        v=[]
        	w=[]
        	for l in range(len(Ind)):
			r=[]
                	for j in range(len(p)):
                        	r.append(p[j][0][l])
                	f=np.mean(r)
                	u.append(f)
                	e=[]
                	for n in r:
                        	s=n**-6.0
                        	e.append(s)
                	k=np.mean(e)**(-1./6.)
                	w.append(k)

        	np.savetxt("NOE/average_whole_state%d.txt"%i,u)
        	np.savetxt("NOE/rminus6_whole_state%d.txt"%i,w)	# rminus6 file will be used in BICePs as model distances


