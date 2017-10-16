#!/bin/bash

# -s N -t C
# prep files and run allsteps
#for i in EPR3; do
#    cd $i
#    python ~/research/repos/scripts/Allsteps_VAV.py $i.mol2 $i CappingAtoms.dat X G 0 &> allsteps.log # runs allsteps
#    cd ..; done

#mkdir tmp; cp EPR3/EPR3.off tmp; cd tmp
cd tmp
    # Build tleap script.
#echo source ~tud67309/local/amber11/dat/leap/cmd/leaprc.ff99SBnmr > build.tleap
#echo source leaprc.gaff >> build.tleap
#echo gaff = loadamberparams gaff.dat >> build.tleap
#echo loadoff EPR3.off >> build.tleap
#echo H035 = sequence { LEU EPR3 LEU EPR3 LEU EPR3 } >> build.tleap
#echo bond H035.1.N H035.6.C >> build.tleap
#echo saveAmberParm H035 H035.prmtop H035.crd >> build.tleap
#echo quit >> build.tleap

    # Run the tleap script
tleap -f build.tleap

    # Run Acpype
python ~/research/scripts/acpype.py -p H035.prmtop -x H035.crd -b H035

cd ..
