import os, sys, glob, copy


def InsertGBSAParms(TopFile, newTopFile):
    """inserts a collection of GBSA parameters for GAFF atomtypes into the 
    appropriate place into the GMX topology file.


    NOTE:  if you find there are missing parameters here, it is
    VERY easy to add more to this string!  The parameters are
    based (in most cases) on the atom, and are completely
    analogous to those in the $GMXLIB/amber99sb.ff/gbsa.itp file, e.g."""

    amber99sb_radii_lines = """Br           0.1      1      1        0.125     0.85 ; H
C            0.172    1      1.554    0.1875    0.72 ; C
CA           0.18     1      1.037    0.1875    0.72 ; C
CB           0.172    0.012  1.554    0.1875    0.72 ; C
CC           0.172    1      1.554    0.1875    0.72 ; C
CN           0.172    0.012  1.554    0.1875    0.72 ; C
CR           0.18     1      1.073    0.1875    0.72 ; C
CT           0.18     1      1.276    0.190     0.72 ; C
CV           0.18     1      1.073    0.1875    0.72 ; C
CW           0.18     1      1.073    0.1875    0.72 ; C
C*           0.172    0.012  1.554    0.1875    0.72 ; C
H            0.1      1      1        0.115     0.85 ; H
HC           0.1      1      1        0.125     0.85 ; H
H1           0.1      1      1        0.125     0.85 ; H
HA           0.1      1      1        0.125     0.85 ; H
H4           0.1      1      1        0.115     0.85 ; H
H5           0.1      1      1        0.125     0.85 ; H
HO           0.1      1      1        0.105     0.85 ; H
HS           0.1      1      1        0.125     0.85 ; H
HP           0.1      1      1        0.125     0.85 ; H
N            0.155    1      1.028    0.17063   0.79 ; N
NA           0.155    1      1.028    0.17063   0.79 ; N
NB           0.155    1      1.215    0.17063   0.79 ; N
N2           0.16     1      1.215    0.17063   0.79 ; N
N3           0.16     1      1.215    0.1625    0.79 ; N
O            0.15     1      0.926    0.148     0.85 ; O
OH           0.152    1      1.080    0.1535    0.85 ; O
O2           0.17     1      0.922    0.148     0.85 ; O
S            0.18     1      1.121    0.1775    0.96 ; S
SH           0.18     1      1.121    0.1775    0.96 ; S""".split('\n')

    radii = {}  # {atomtype: line[2:] }
    # parse the GBSA parms for AMBER atomtypes
    for line in amber99sb_radii_lines:
        radii[line[0:2]] = line[2:]
    # extrapolate for GAFF atomtypes
    radii['c3'] = copy.deepcopy(radii['CT'])
    radii['c2'] = copy.deepcopy(radii['C '])
    radii['cc'] = copy.deepcopy(radii['C '])
    radii['cd'] = copy.deepcopy(radii['C '])
    radii['ce'] = copy.deepcopy(radii['C '])
    radii['cf'] = copy.deepcopy(radii['C '])
    radii['cp'] = copy.deepcopy(radii['C '])
    radii['c_'] = copy.deepcopy(radii['C '])
    radii['ha'] = copy.deepcopy(radii['HA'])
    radii['hc'] = copy.deepcopy(radii['HC'])
    radii['hn'] = copy.deepcopy(radii['H '])
    radii['h1'] = copy.deepcopy(radii['H1'])
    radii['ho'] = copy.deepcopy(radii['HO'])
    radii['oh'] = copy.deepcopy(radii['OH'])
    radii['os'] = copy.deepcopy(radii['O '])  # this is a fudge -- no GB radii for OS?!
    radii['n '] = copy.deepcopy(radii['N '])
    radii['n2'] = copy.deepcopy(radii['N '])
    radii['na'] = copy.deepcopy(radii['N '])
    radii['nd'] = copy.deepcopy(radii['N '])
    radii['n3'] = copy.deepcopy(radii['N3'])
    radii['c '] = copy.deepcopy(radii['C '])
    radii['o '] = copy.deepcopy(radii['O '])

    radii['ca'] = copy.deepcopy(radii['CA']) #sm

    fin = open(TopFile,'r')
    lines = fin.readlines()
    fin.close()

    # first, let's find *ALL* the atom types in the topology file
    i = 0 
    while lines[i].count("[ atomtypes ]") == 0:
        i += 1
    i += 2
    topfile_atomtypes = []
    while lines[i].strip() != '':
        #topfile_atomtypes.append( lines[i][0:2] ) #am2gmx 
        topfile_atomtypes.append( lines[i][1:3] )  #acpype
        i += 1

    # check that atom types are read in correctly
    print topfile_atomtypes

    # next, we'll insert the appropriate GBSA lines for each atomtype
    # in the topfile
    i = 0
    while lines[i].count( 'moleculetype' ) == 0:
        i+=1

    insertText = """[ implicit_genborn_params ]

; atype      sar      st     pi       gbr       hct
; for GAFF atomtypes from amb2gmx.pl\n"""

    for atomtype in topfile_atomtypes:
        insertText += (atomtype + radii[atomtype] +'\n')
    insertText += '\n'

    lines.insert(i,insertText)

    fout = open(newTopFile,'w')
    fout.writelines(lines)
    fout.close()

if __name__ == '__main__':

    usage = """Usage:  python InsertGBSAParms.py OldTopFile NewTopFile

    Inserts a collection of GBSA parameters for GAFF atomtypes into the 
    appropriate place into the GMX topology file, and writed a new GMX topology file.

    NOTE:  if you find there are missing parameters here, it is
    VERY easy to add these to this script (see source code). """

    if len(sys.argv) < 3:
        print usage
        sys.exit(1)

    OldTopFile = sys.argv[1]
    NewTopFile = sys.argv[2]
   
    print 'Running InsertGBSAParms - ' + OldTopFile + ' ' + NewTopFile
    InsertGBSAParms(OldTopFile, NewTopFile)
    


