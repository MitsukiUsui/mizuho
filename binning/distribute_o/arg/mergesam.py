#!/usr/bin/env python3

import pandas as pd

def main(assemListFilepath, numBins,  distDirec):
    assem_df=pd.read_csv(assemListFilepath)
    numAssem=assem_df.shape[0]

    for binId in range(1, numBins + 1):
        binDirec="{}/bin{:03d}".format(distDirec, binId)
        samFilepath_lst=["{}/{}.sam".format(binDirec, assemName) for assemName in assem_df["assembly_name"]]
        mergeFilepath="{}/original.bam".format(binDirec)
        print("{},{},{}".format(numAssem, ",".join(samFilepath_lst), mergeFilepath))

if __name__=="__main__":
    assemListFilepath="../list/assembly.list"
    numBins=173
    distDirec="/work/GoryaninU/mitsuki/out/binning/distribute"
    main(assemListFilepath, numBins, distDirec)
