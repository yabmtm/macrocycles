import os, sys
import copy
import numpy as np


usage = """Usage:  python get_replica_indices.py mdlogfile ntemps

    Outputs an array of replica indices to follow replicas though temperature space:
    NOTE: Makes output files <mdlogfile>_replex.txt and <mdlogfile>_replex.dat

    Example: python get_replica_indices.py md0.log 24

"""

if len(sys.argv) < 3:
   print usage
   sys.exit(1)


mdlogfile = sys.argv[1] 
ntemps = int(sys.argv[2])

# First, let's grep the exchanges out of the log file
txtfile = mdlogfile + '_replex.txt'
os.system('cat %s | grep "Repl ex" >  %s'%(mdlogfile,txtfile))


# Next, read in the text file and parse it to make a data file
if (True):
    fin = open(txtfile,'r')
    lines = fin.readlines()
    fin.close()

    # Example:
    # Repl ex  0    1    2 x  3    4    5    6    7    8 x  9   10 x 11   12 x 13   14 x 15   16 x 17   18 x 19   20 x 21   22   23
    # Repl ex  0    1 x  2    3 x  4    5 x  6    7    8    9 x 10   11 x 12   13 x 14   15 x 16   17 x 18   19 x 20   21   22   23
    # ...

    replica_indices = []
    replica_indices.append( range(ntemps) )

    print replica_indices[-1]

    for line in lines:

        # print 'line', line

        # find the exchanges
        exchange_these = []
        fields = line.strip().split()
        for i in range(len(fields)-1):
            if fields[i] == 'x':
                exchange_these.append( [int(fields[i-1]), int(fields[i+1])] )
                 
        # calculate the new replica indices
        new_indices = copy.copy(replica_indices[-1])
        for pair in exchange_these:
            new_indices[pair[0]], new_indices[pair[1]] = new_indices[pair[1]], new_indices[pair[0]]

        # add them to the tally 
        replica_indices.append( new_indices )

    outfn = mdlogfile + '_replex.dat'
    print 'Saving', outfn, '...',
    np.savetxt(outfn, np.array(replica_indices), fmt='%d')
    print 'Done.'

