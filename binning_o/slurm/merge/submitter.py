#!/usr/bin/env python3

import os
import pandas as pd
from myutil.myutil import myrun

def main(baseDirec, numBins):
    for binId in range(1, numBins + 1):
        binDirec = "{}/bin{:03d}".format(baseDirec, binId)
        outLeftFilepath="{}/bin{:03d}_R1.fastq".format(binDirec, binId)
        outRightFilepath="{}/bin{:03d}_R2.fastq".format(binDirec, binId)
        cmd = "sbatch caller.sh {} {} {}".format(binDirec, outLeftFilepath, outRightFilepath)
        myrun(cmd)
            
if __name__=="__main__":
    baseDirec="/work/GoryaninU/mitsuki/out/binning/bin"
    numBins=184
    main(baseDirec, numBins)
