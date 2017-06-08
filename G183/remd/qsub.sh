#!/bin/bash
#PBS -l walltime=12:00:00
#PBS -N yang3_Nspe_only 
#PBS -q normal
#PBS -l nodes=4:ppn=12
#PBS -o yang3_Nspe_only 
#PBS -j oe
#PBS
#

module load gromacs
#module use -a /home/tuf10875/pkg/modulefiles/
#module load gromacs/4.6.7-static
#module load gromacs/5.1.2

cd $PBS_O_WORKDIR

## Normal runs
${MPI_BIN}/mpiexec -np 48 mdrun_mpi -s prod_.tpr -multi 24 -replex 5000 -c conf_prod.gro -maxh 12

