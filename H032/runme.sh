#!/bin/bash

# -s N -t C
# prep files and run allsteps
#for i in EPR3; do
#    cd $i
#    python ~/research/repos/scripts/Allsteps_VAV.py $i.mol2 $i CappingAtoms.dat X G 0 &> allsteps.log # runs allsteps
#    cd ..; done

mkdir tmp; cp EPR1/EPR1.off tmp; cd tmp
cd tmp
    # Build tleap script.
echo source leaprc.ff99SB > build.tleap
echo source leaprc.gaff >> build.tleap
echo gaff = loadamberparams gaff.dat >> build.tleap
echo loadoff EPR1.off >> build.tleap
echo H032 = sequence { LEU EPR1 LEU EPR1 LEU EPR1 } >> build.tleap
echo bond H032.1.N H032.6.C >> build.tleap
echo saveAmberParm H032 H032.prmtop H032.crd >> build.tleap
echo quit >> build.tleap

    # Run the tleap script
tleap -f build.tleap

    # Run Acpype
python ~/research/scripts/acpype.py -p H032.prmtop -x H032.crd -b H032

cd ..
