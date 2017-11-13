#!/usr/bin/env python3

import pandas as pd
import sys
from myutil.myutil import myrun

def main(listFilepath):
    list_df=pd.read_csv(listFilepath, header=None)
    for assemname in list_df[0]:
        correctDirec="/work/GoryaninU/mitsuki/out/spades/mizuho/{}/corrected".format(assemname)
        filterDirec="/work/GoryaninU/mitsuki/out/spades/mizuho/{}/filtered".format(assemname)
        cl="{}/{}_R1.00.0_0.cor.fastq.gz".format(correctDirec, assemname)
        cr="{}/{}_R2.00.0_0.cor.fastq.gz".format(correctDirec, assemname)
        fl="{}/{}_R1.fastq".format(filterDirec, assemname)
        fr="{}/{}_R2.fastq".format(filterDirec, assemname)
        cmd="sbatch filter.sh {} {} {} {}".format(cl, cr, fl, fr)
        myrun(cmd)

if __name__=="__main__":
    listFilepath="../assembly.list"
    main(listFilepath)
