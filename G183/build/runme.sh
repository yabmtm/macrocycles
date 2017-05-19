#!/bin/bash


# prep files and run allsteps
#for i in EPR MOE; do
#    cd $i
#    python ~/research/repos/voelzlab/custom_topologies/scripts/Allsteps_VAV.py $i.mol2 $i CappingAtoms.dat X G 0 && sleep 5 # runs allsteps
#    cd ..; done

mkdir tmp; cp EPR/EPR.off tmp
cp MOE/MOE.off tmp; cp EPR2/EPR2.off tmp; cd tmp

    # Build tleap script.
echo source leaprc.gaff >> build.tleap
echo gaff = loadamberparams gaff.dat >> build.tleap
echo loadoff MOE.off >> build.tleap
echo loadoff EPR.off >> build.tleap
echo loadoff EPR2.off >> build.tleap
echo G182 = sequence { MOE EPR MOE EPR2 MOE EPR } >> build.tleap
echo bond G182.1.N G182.6.C >> build.tleap
echo saveAmberParm G182 G182.prmtop G182.crd >> build.tleap
echo quit >> build.tleap

    # Run the tleap script
tleap -f build.tleap

    # Run Acpype
python ~/research/scripts/acpype.py -p G182.prmtop -x G182.crd -b G182

cd ..
