#!/bin/bash

# load in off files of spiroligomer/peptoid, make complete topology and output to Gromacs format
mkdir tmp
cp MOE/MOE.off tmp
cp EPR1/EPR1.off tmp; cd tmp

    # Build tleap script.
echo source leaprc.gaff >> build.tleap
echo gaff = loadamberparams gaff.dat >> build.tleap
echo loadoff MOE.off >> build.tleap
echo loadoff EPR1.off >> build.tleap
echo QPM1 = sequence { MOE EPR1 MOE EPR1 MOE EPR1 } >> build.tleap
echo bond QPM1.1.N QPM1.6.C >> build.tleap
echo saveAmberParm QPM1 QPM1.prmtop QPM1.crd >> build.tleap
echo quit >> build.tleap

    # Run the tleap script
tleap -f build.tleap

    # Run Acpype
python ~/scripts/acpype.py -p QPM1.prmtop -x QPM1.crd -b QPM1
cd ..
