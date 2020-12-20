#!/bin/bash

for i in NIB; do
    cd $i
    python ~/research/repos/scripts/Allsteps_VAV.py $i.mol2 $i CappingAtoms.dat X G 0 &> allsteps.log # runs allsteps
    cd ..; done

mkdir tmp; cp EPR1/EPR1.off tmp
cp NIB/NIB.off tmp; cd tmp

    # Build tleap script.
echo source leaprc.gaff >> build.tleap
echo gaff = loadamberparams gaff.dat >> build.tleap
echo loadoff EPR1.off >> build.tleap
echo loadoff NIB.off >> build.tleap
echo QPM3 = sequence { NIB EPR1 NIB EPR1 NIB EPR1 } >> build.tleap
echo bond QPM3.1.N QPM3.6.C >> build.tleap
echo saveAmberParm QPM3 QPM3.prmtop QPM3.crd >> build.tleap
echo quit >> build.tleap

    # Run the tleap script
tleap -f build.tleap

    # Run Acpype
python ~/research/scripts/acpype.py -p QPM3.prmtop -x QPM3.crd -b QPM3

cd ..
