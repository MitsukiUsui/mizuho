#!/usr/bin/env python3

import os
import yaml
import pandas as pd
from myutil.myutil import myrun

def main(assemListFilepath, numBins):
    assem_df=pd.read_csv(assemListFilepath, header=None)
    for _, row in assem_df.iterrows():
        if row[0]!="all":
            assemName=row[0]
            for binId in range(1, numBins + 1):
                inFilepath="/work/GoryaninU/mitsuki/out/binning/bowtie/{}.sam".format(assemName)
                outFilepath="/work/GoryaninU/mitsuki/out/binning/bin/bin{:03d}/{}.sam".format(binId, assemName)
                cmd="sbatch caller.sh {} {}".format(inFilepath, outFilepath)
                myrun(cmd)
            
if __name__=="__main__":
    assemListFilepath="../../list/assembly.list"
    numBins=184
    main(assemListFilepath, numBins)
