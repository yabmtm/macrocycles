#!/usr/bin/env python

import sys, os
import random, math, string, tempfile
import numpy as np

usage = """runme_implicit_REMD.py GROFILE TOPFILE INNDXFILE TITLE
   Continues an equilibrated gromacs simulation, using REMD from an equilibrated GROFILE and TOPFILE and INDEXFILE.
   TITLE specifies the jobname, usually the name of the protein and mutant you are simulating. 
   Try: >>> python runme_implicit_REMD.py conf_equilibrated.gro pep_withgaffGBSA.top 7mer_1_2.000 """

if len(sys.argv) < 3:
    print usage
    sys.exit(1)

GroFile = sys.argv[1]
TopFile = sys.argv[2]
IndexFile = sys.argv[3]
JobTitle = sys.argv[4]


# DEBUG flag:
DEBUG = True
TESTING = False  # if True, print cmds but dpn't run them

def cleanup():
    """Delete files not needed."""

    os.system('rm *.gro; rm *.ndx; rm *.log')
    os.system('rm *.top; rm *.tpr')
    os.system('rm step*')
    os.system('rm ./#*')

def run_cmd(cmd, testing=False):
    """Execute command-line command."""

    print '>>', cmd
    if not testing:
        os.system(cmd)

def write_production_mdp(prefix, rep, temp):
    """Write a production mdp file "prefix"_<rep>.mdp with temperature temp."""

    fn = prefix + '_%d.mdp'%rep
    fout = open(fn, 'w')
    fout.write("""title                    = prod_GBSA
cpp                      = /lib/cpp
include                  = -I../top
define                   = 
integrator               = sd
dt                       = 0.002
nsteps                   = 25000000   ; 50 ns
nstxout                  = 500000  ; every 1 ns 
nstvout                  = 500000
nstlog                   = 5000 ; every 10 ps
nstxtcout                = 5000  ; every 10 ps
nstenergy                = 5000  ; every 10 ps


implicit_solvent = GBSA
gb_algorithm     = OBC
nstgbradii       = 1
gb_epsilon_solvent = 80.0
sa_algorithm    = Ace-approximation

comm_mode = ANGULAR

rgbradii         = 0.9
coulombtype     = Cut-off
rvdw            = 0.9
rlist           = 0.9
rcoulomb        = 0.9

; CONSTRAINTS
constraints     = hbonds
constraint_algorithm = LINCS

; other stuff
bd_fric        = 1.0
nstcomm                  = 10
comm_grps                = System
xtc_grps                 = System
energygrps               = System
nstlist                  = 10
ns_type                  = grid
tc-grps                  = System 
tau_t                    = 0.0109

ref_t                    = %d 
compressibility          = 4.5e-5
ref_p                    = 1.0
gen_vel                  = yes
gen_temp                 = %d 
gen_seed                 = 1729
pbc                      = no"""%(temp, temp))

    fout.close()

    return fn

 
def logSpacedTemps(T_min, T_max, ntemps):
    """Return a list of ntemps temperatures linearly-spaced on a log-scale."""
    return [ T_min + (T_max - T_min) * (np.exp(float(i) / float(ntemps-1)) - 1.0) / (np.e - 1.0) for i in range(ntemps) ]



#-----------------------------------
# MAIN
#-----------------------------------

# cleanup()  # cleanup from last time

ntemps = 24 
Tmin, Tmax = 300.0, 800.0
temps = np.round(logSpacedTemps(Tmin, Tmax, ntemps))
print 'temps', temps

# Set up Production runs  for all temps
for rep in range(len(temps)):
    temp = temps[rep]
    mdpfilename = write_production_mdp("prod", rep, temp)
    run_cmd( 'grompp -f %s -c %s -p %s -n %s -o prod_%d.tpr'%(mdpfilename, GroFile, TopFile, IndexFile, rep), testing=TESTING )

# write a qsub script to the rundir
qsubfile = 'qsub.sh'

if (1):
    ### normal queue ###
    nprocs_per_temp = 2
    nprocs = ntemps*nprocs_per_temp 
    queue = 'normal' 
    ppn = 12   # nprocs_per_node
    nnodes = nprocs/ppn 

if (0):
    ### legacy queue ###
    nprocs = 8 
    queue = 'legacy'
    ppn = 8
    nnodes = ntemps/ppn

if (0):
    ### devel queue ###
    nprocs = 8 
    queue = 'devel'
    ppn = 8
    nnodes = ntemps/ppn

walltime = '12:00:00'
jobname = JobTitle 

fout = open(qsubfile,'w')
fout.write("""#!/bin/bash
#PBS -l walltime=%s
#PBS -N %s 
#PBS -q %s
#PBS -l nodes=%d:ppn=%d
#PBS -o %s 
#PBS -j oe
#PBS
#

module load gromacs
#module use -a /home/tuf10875/pkg/modulefiles/
#module load gromacs/4.6.7-static
#module load gromacs/5.1.2

cd $PBS_O_WORKDIR

## Normal runs
${MPI_BIN}/mpiexec -np %d mdrun_mpi -s prod_.tpr -multi %d -replex 5000 -c conf_prod.gro -maxh 12

"""%(walltime, jobname, queue, nnodes, ppn, jobname, nprocs, ntemps)   )
fout.close()     # note that we don't need "mpirun -np 12" -- the cluster automatically figures this out

