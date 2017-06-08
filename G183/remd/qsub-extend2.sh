#!/bin/sh
#PBS -l walltime=12:00:00
#PBS -N yang3_Nspe_2
#PBS -q normal 
#PBS -l nodes=4:ppn=12
#PBS -o yang3_Nspe_2.qsub.log
#PBS -j oe
#PBS 

module load gromacs
#use -a /home/tuf10875/pkg/modulefiles/
#module load gromacs/4.6.7-static
#module load gromacs/5.1.2

cd $PBS_O_WORKDIR


# extend tprs for all replicas
tpbconv -s prod_0.tpr -nsteps 25000000.000000 -o prod2_0.tpr
tpbconv -s prod_1.tpr -nsteps 25000000.000000 -o prod2_1.tpr
tpbconv -s prod_2.tpr -nsteps 25000000.000000 -o prod2_2.tpr
tpbconv -s prod_3.tpr -nsteps 25000000.000000 -o prod2_3.tpr
tpbconv -s prod_4.tpr -nsteps 25000000.000000 -o prod2_4.tpr
tpbconv -s prod_5.tpr -nsteps 25000000.000000 -o prod2_5.tpr
tpbconv -s prod_6.tpr -nsteps 25000000.000000 -o prod2_6.tpr
tpbconv -s prod_7.tpr -nsteps 25000000.000000 -o prod2_7.tpr
tpbconv -s prod_8.tpr -nsteps 25000000.000000 -o prod2_8.tpr
tpbconv -s prod_9.tpr -nsteps 25000000.000000 -o prod2_9.tpr
tpbconv -s prod_10.tpr -nsteps 25000000.000000 -o prod2_10.tpr
tpbconv -s prod_11.tpr -nsteps 25000000.000000 -o prod2_11.tpr
tpbconv -s prod_12.tpr -nsteps 25000000.000000 -o prod2_12.tpr
tpbconv -s prod_13.tpr -nsteps 25000000.000000 -o prod2_13.tpr
tpbconv -s prod_14.tpr -nsteps 25000000.000000 -o prod2_14.tpr
tpbconv -s prod_15.tpr -nsteps 25000000.000000 -o prod2_15.tpr
tpbconv -s prod_16.tpr -nsteps 25000000.000000 -o prod2_16.tpr
tpbconv -s prod_17.tpr -nsteps 25000000.000000 -o prod2_17.tpr
tpbconv -s prod_18.tpr -nsteps 25000000.000000 -o prod2_18.tpr
tpbconv -s prod_19.tpr -nsteps 25000000.000000 -o prod2_19.tpr
tpbconv -s prod_20.tpr -nsteps 25000000.000000 -o prod2_20.tpr
tpbconv -s prod_21.tpr -nsteps 25000000.000000 -o prod2_21.tpr
tpbconv -s prod_22.tpr -nsteps 25000000.000000 -o prod2_22.tpr
tpbconv -s prod_23.tpr -nsteps 25000000.000000 -o prod2_23.tpr

## Normal runs
${MPI_BIN}/mpiexec -np 48 mdrun_mpi -s prod2_.tpr -cpi -multi 24 -replex 5000 -c conf_prod2.gro -maxh 12
