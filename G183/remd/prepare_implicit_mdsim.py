#!/usr/bin/env python

import sys, os
import random, math, string, tempfile, copy

from InsertGBSAParms import InsertGBSAParms

usage = """prepare_implicit_mdsim.py [PdbFile/GroFile] TopFile outname

   Prepares a gromacs simulation from either a PDB or *.gro
   structure and corresponding *.top GMX topology file.

   Protocol:
       Minimization 	(mdp/minimize_GBSA.mdp)
       Equilibration 	(mdp/equil_GBSA.mdp)
       Production Prep 	(mdp/prod_GBSA.mdp)

   Writes:
       outname.gro
       outname.top
       outname.ndx
       outname.tpr

   NOTES:
       1) to adjust the simulation parameters, edit the mdp files
       2) uses ./tmp directory in current working dir 
"""

DEBUG = True
TESTING = False  # if True, print cmds but dpn't run them


def run_cmd(cmd, testing=False):
    """Execute command-line command."""

    print '>>', cmd
    if not testing:
        os.system(cmd)

class GromacsWorkspace(object):
    """An object to store all info necessary to minimize, equilibrate etc. in a temporary directory."""

    def __init__(self, tmpdir, StructureFile, TopologyFile, mdpdir, outname='out', nthreads=1, testing=False):
        """Initialize the class."""

        self.tmpdir = os.path.abspath(tmpdir)
        self.origdir = os.path.abspath(os.curdir)
        self.mdpdir = mdpdir
        self.StructureFile = os.path.abspath(StructureFile)
        self.TopologyFile = os.path.abspath(TopologyFile)
        self.outpath = os.path.abspath(outname)
        self.outname = os.path.basename(outname)
        self.nthreads = nthreads
        self.testing = testing

        self.TESTING = False  # For debugging

        # Create the tmp directory 
        if not os.path.exists(self.tmpdir):
            os.mkdir(self.tmpdir)

        # Create a set of relevant temporary filenames
        self.SetFilenames()

    def SetFilenames(self):

        # Create relevant temporary filenames
        if self.StructureFile[-4:] == '.gro':
            self.newGroFile = os.path.join(self.tmpdir, os.path.basename(self.StructureFile.replace('.gro','_pbc.gro')))
        elif self.StructureFile[-4:] == '.pdb':
            self.newGroFile = os.path.join(self.tmpdir, os.path.basename(self.StructureFile).replace('.pdb','_pbc.gro'))
        else:
            print 'Do not understand Infile =', self.StructureFile, ' -- Must be *.pdb or *.gro.'
            sys.exit(1)

        self.indexFile = os.path.join(self.tmpdir, '%s.ndx'%self.outname)     
        self.newTopFile = os.path.join(self.tmpdir, os.path.basename(self.TopologyFile).replace('.top','_withgaff.top'))

        self.mdp_minimization   = os.path.join(self.mdpdir, 'minimize_GBSA.mdp')
        self.mdp_equilibration  = os.path.join(self.mdpdir, 'equil_GBSA.mdp')
        self.mdp_production     = os.path.join(self.mdpdir, 'prod_GBSA.mdp')

        self.tpr_minimization  = os.path.join(self.tmpdir, '%s_minimize.tpr'%self.outname)
        self.tpr_equilibration = os.path.join(self.tmpdir, '%s_equil.tpr'%self.outname)
        self.tpr_production    = os.path.join(self.tmpdir, '%s.tpr'%self.outname)

        self.outgro_minimization = os.path.join(self.tmpdir, '%s_minimized.gro'%self.outname)
        self.outgro_equilibration = os.path.join(self.tmpdir, '%s_minimized.gro'%self.outname)
        self.outgro_production = os.path.join(self.tmpdir, '%s.gro'%self.outname)


    def run_cmd(self, cmd):
        """Execute command-line command."""

        print '>>', cmd
        if not self.testing:
            os.system(cmd)


    def build_implicit(self):
        """Execute the steps of building an implicit-solvent GBSA files for prodution runs."""

        # change to working in the tmp directory
        os.chdir(self.tmpdir)

        # Make a huge PBC box, so Gromacs won't get confused
        self.run_cmd( " editconf -f %s -o %s -box 4 4 4"%(self.StructureFile, self.newGroFile))

        # make an index file
        self.run_cmd( "echo 'q\n' | make_ndx -f %s -o %s"%(self.newGroFile, self.indexFile))

        # insert GBSA parameters for the GAFF atomtypes into the *.top file
        InsertGBSAParms(self.TopologyFile, self.newTopFile)

        # Minimize the system
        self.run_cmd( 'grompp -f %s -c %s -p %s -n %s -o %s'%(self.mdp_minimization, self.newGroFile, self.newTopFile, 
                                                              self.indexFile, self.tpr_minimization) )
        self.run_cmd( 'mdrun -nt 1 -v -s %s -c %s'%(self.tpr_minimization, self.outgro_minimization) )

        # Equilibrate the system
        self.run_cmd( 'grompp -f %s -c %s -p %s -n %s -o %s'%(self.mdp_equilibration, self.outgro_minimization,
                                                              self.newTopFile, self.indexFile, self.tpr_equilibration) )
        self.run_cmd( 'mdrun -v -nt %d -s %s -c %s'%(self.nthreads, self.tpr_equilibration, self.outgro_equilibration) )

        # create a Production run *.tpr
        self.run_cmd( 'grompp -f %s -c %s -p %s -n %s -o %s'%(self.mdp_production, self.outgro_equilibration,
                                                              self.newTopFile, self.indexFile, self.tpr_production) )

        # change back to the original directory
        os.chdir(self.origdir)

        # copy final version of files to path specified by outname
        self.run_cmd('cp %s %s'%(self.outgro_equilibration, self.outpath+'.gro'))
        self.run_cmd('cp %s %s'%(self.tpr_production, self.outpath+'.tpr'))
        self.run_cmd('cp %s %s'%(self.indexFile, self.outpath+'.ndx'))
        self.run_cmd('cp %s %s'%(self.newTopFile, self.outpath+'.top'))



# ------------------------ Main program -----------------------------------

if len(sys.argv) < 3:
    print usage
    sys.exit(1)


StructureFile = sys.argv[1]
TopFile = sys.argv[2]
outname = sys.argv[3]

# Create a tmp directory 
tmpdir = 'tmp'
if not os.path.exists(tmpdir):
    os.mkdir(tmpdir)

# The default mdp directory is in the same location as this script
mdpdir = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]),'mdp'))

g = GromacsWorkspace(tmpdir, StructureFile, TopFile, mdpdir, outname=outname, nthreads=1)
g.build_implicit()

