#!/bin/bash

# -s N -t C
# prep files and run allsteps
#for i in EPR1; do
#    cd $i
#    python ~/research/repos/scripts/Allsteps_VAV.py $i.mol2 $i CappingAtoms.dat X G 0 &> allsteps.log # runs allsteps
#    cd ..; done

mkdir tmp
cp MOE/MOE.off tmp
cp EPR1/EPR1.off tmp; cd tmp

    # Build tleap script.
echo source leaprc.gaff >> build.tleap
echo gaff = loadamberparams gaff.dat >> build.tleap
echo loadoff MOE.off >> build.tleap
echo loadoff EPR1.off >> build.tleap
echo H030 = sequence { MOE EPR1 MOE EPR1 MOE EPR1 } >> build.tleap
echo bond H030.1.N H030.6.C >> build.tleap
echo saveAmberParm H030 H030.prmtop H030.crd >> build.tleap
echo quit >> build.tleap

    # Run the tleap script
tleap -f build.tleap

    # Run Acpype
python ~/research/scripts/acpype.py -p H030.prmtop -x H030.crd -b H030

cd ..
