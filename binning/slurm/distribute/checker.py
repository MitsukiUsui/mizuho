#!/usr/bin/env python3

import os
import pandas as pd
from myutil.myutil import myrun

def main(pairListFilepath, binDirec, numBins):
    pair_df=pd.read_csv(pairListFilepath, header=None)
    
    for _, row in pair_df.iterrows():
        sampleId=row[0]
        failed=False
        for binId in range(1, numBins + 1):
            for direction in ("R1", "R2"):
                filepath="{0}/bin{1:03d}/{2}_{3}.fastq".format(binDirec, binId, sampleId, direction)
                if not(os.path.exists(filepath)):
                    failed=True
        if failed:
            print(sampleId)

            
if __name__=="__main__":
    pairListFilepath="../../list/pair.list"
    binDirec="/work/GoryaninU/mitsuki/out/binning/bin"
    numBins=184
    main(pairListFilepath, binDirec, numBins)
