#!/bin/sh
#PBS -l walltime=2:00:00
#PBS -N test_H030 
#PBS -q normal 
##PBS -l mem=300gb
#PBS -l nodes=1:ppn=1
#PBS -o test_H030 
#PBS 

cd $PBS_O_WORKDIR

bash runme
