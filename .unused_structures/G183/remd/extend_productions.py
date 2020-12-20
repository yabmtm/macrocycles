#!/usr/bin/env python 

# Extends gromacs production runs. Must be run in folder with existing prodX_X.tpr files with a specified sequence name
# Note: Must use the same number of cpus/replica as in the starting simulation 

import os, sys, commands
import numpy as np

#jobprefix = commands.getoutput("basename $PWD")
#print 'Running in folder ',jobprefix
jobprefix = 'yang3_Nspe'

# Since int rounds down, this will automatically continue a half finished job that crashed
# USE first_new_round = 2 when extending for the first time
first_new_round = 32
last_round = 51 
print 'Attempting to extend starting with round %d'%(first_new_round)


newrounds = range(first_new_round, last_round+1)  # Run for additional rounds (each round is a new job)
firstround = newrounds[0]

nsteps      = 25000000 # 50 ns 
extendby    = 50000.0  # number of ps to extend (50 ns)
swapsteps   =  5000 # number of (2 fs)-timesteps to exchange replicas (10 ps)
print 'Running %d additional rounds' % len(newrounds)

# Queue information
nreplicas = 24
queue = 'normal'

if (queue == 'manycore'):
    ppn = 48 # num cores
    maxh = 24 # max queue runtime allowed
elif (queue == 'legacy' or queue == 'gpu' or queue == 'highmem'):
    ppn = 8
    maxh = 24
elif (queue == 'devel'):
    ppn = 8
    maxh = 12

elif (queue == 'normal'):
    ### cb2rr normal queue ###
    nprocs_per_temp = 2
    nprocs = nreplicas*nprocs_per_temp
    queue = 'normal'
    ppn = 12   # nprocs_per_node 12 for owlsnest, 20 for cb2rr
    nnodes = nprocs/ppn
    #nnodes = int(np.ceil(float(nprocs)/float(ppn)))   # <-- fix because using 20 replicas from cb2rr
    maxh = 12
else:
    print 'Unrecognised queue ', queue
    sys.exit(1)

walltime = str(maxh) + ':00:00'
nnodes = nprocs/ppn    # Num of nodes to request from queue
if (nnodes < 1):
   nnodes = 1
nproc = nnodes * ppn  # Used for mpirun -np flag

print 'Submitting job %s to %s queue on %s nodes with %s procs each' % (jobprefix,queue,nnodes,ppn)
previousJobID = None

# Loop over all the additional round and write a qsub script for each new round
for newround in newrounds:
    jobname = jobprefix + '_%d'%newround
    print 'Writing qub-extend%d.sh'%newround

    # Make a qsub script and submit it
    qsub_txt = """#!/bin/sh
#PBS -l walltime=%s
#PBS -N %s
#PBS -q %s 
#PBS -l nodes=%d:ppn=%d
#PBS -o %s.qsub.log
#PBS -j oe
"""%(walltime, jobname, queue, nnodes, ppn, jobname)

    if previousJobID != None:
        qsub_txt += '#PBS -W depend=afterok:%d\n'%previousJobID

    qsub_txt += """#PBS 

module load gromacs
#use -a /home/tuf10875/pkg/modulefiles/
#module load gromacs/4.6.7-static
#module load gromacs/5.1.2

cd $PBS_O_WORKDIR

"""

# -nsteps      int    0       Change the number of steps
# -time        real   -1      Continue from frame at this time (ps) instead of
#                             the last frame

    qsub_txt += '\n# extend tprs for all replicas\n'
    for i in range(nreplicas):

        if newround == firstround:

            if firstround == 2:
                cmd = 'tpbconv -s prod_%d.tpr -nsteps %f -o prod%d_%d.tpr'%(i, nsteps, newround, i)
                qsub_txt += cmd+'\n'
                print 'Extend Round #2:', cmd

            else:
                cmd = 'tpbconv -s prod%d_%d.tpr -nsteps %f -o prod%d_%d.tpr'%(newround-1, i, nsteps*newround, newround, i)
                if (i==0):  #Only print for first temp replica
                    print 'Extending first round:', cmd
                qsub_txt += cmd+'\n'

        else: 
            cmd = 'tpbconv -s prod%d_%d.tpr -nsteps %f -o prod%d_%d.tpr'%(newround-1, i, nsteps*newround, newround, i)
            if (i==0):  #Only print for first temp replica
                print 'Extending:', cmd
            qsub_txt += cmd+'\n'

    qsub_txt += '\n'
    qsub_txt += """## Normal runs
${MPI_BIN}/mpiexec -np %d mdrun_mpi -s prod%d_.tpr -cpi -multi %d -replex %d -c conf_prod%d.gro -maxh %d
"""%(nproc, newround, nreplicas, swapsteps, newround,maxh)

    # write the qsub file
    qsubfile = 'qsub-extend%d.sh'%newround
    fout = open(qsubfile, 'w')
    fout.write(qsub_txt)
    fout.close()

    # submit the qsub job
    output = commands.getoutput('qsub '+qsubfile)

    # parse the output to get the jobID 
    previousJobID = int(output.split('.')[0])

