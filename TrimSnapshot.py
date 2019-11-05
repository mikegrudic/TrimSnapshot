#!/usr/bin/env python

# usage: TrimSnapshot.py file1 file2 file3 file4...
# ACHTUNG: This will irreversibly alter the snapshot files you run it on! Be absolutely sure you wanna do this.
# ACHTUNG ACHTUNG: This uses every available thread. Don't run it on the head node :P

from sys import argv
import h5py
import numpy as np
import multiprocessing 
from multiprocessing import Pool
from shutil import move
from os import system
nproc = multiprocessing.cpu_count()

stuff_to_skip = "Metallicity", "DivergenceOfMagneticField", "DivBcleaningFunctionPhi", "DivBcleaningFunctionGradPhi", "StarFormationRate", "BH_Dist"

def CompressFile(f):
    print(f)
    if "_t.hdf5" in f:
        system("rm " + f)
        return
    F = h5py.File(f,'r')
    if not "Header" in F.keys(): return
    f2name = f.replace(".hdf5","_t.hdf5")
    F2 = h5py.File(f2name,'w')
    F.copy("Header", F2)
    for k in F.keys():
        if k=="Header": continue
        F2.create_group(k)
        for k2 in F[k].keys():
            if k2 in stuff_to_skip: continue
            F2[k].create_dataset(k2, data=F[k][k2], compression="gzip", fletcher32=True, shuffle=True, chunks=True)

    F2.close()
    F.close()
    move(f2name, f)
    
if __name__ == "__main__":
    filenames = (f for f in argv[1:])
    Pool(nproc).map(CompressFile, filenames)

