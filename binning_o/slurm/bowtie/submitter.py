#!/usr/bin/env python3

import os
import pandas as pd
from myutil.myutil import myrun

def main(assemListFilepath, pairListFilepath):
    assem_df=pd.read_csv(assemListFilepath, header=None)
    pair_df=pd.read_csv(pairListFilepath, header=None)
    
    for _, row in pair_df.iterrows():
        sampleId=row[0]
        leftFilepath=row[1]
        rightFilepath=row[2]
        outDirec="/work/GoryaninU/mitsuki/out/binning/bowtie/{}".format(sampleId)
        os.makedirs(outDirec, exist_ok=True)

        for _, row in assem_df.iterrows():
            assemname=row[0]
            dbFilepath="/work/GoryaninU/mitsuki/bowtie/mizuho/{}".format(assemname)
            samFilepath="{}/{}.sam".format(outDirec, assemname)
            cmd = "sbatch bowtie.sh {} {} {} {}".format(dbFilepath, leftFilepath, rightFilepath, samFilepath)
            myrun(cmd)
            
if __name__=="__main__":
    assemListFilepath="./list/assembly.list"
    pairListFilepath="./list/pair.list"
    main(assemListFilepath, pairListFilepath)
