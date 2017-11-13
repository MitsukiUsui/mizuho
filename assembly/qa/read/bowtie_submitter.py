#!/usr/bin/env python3

import pandas as pd
import sys
from myutil.myutil import myrun

def main(listFilepath):
    list_df=pd.read_csv(listFilepath, header=None)
    for assemname in list_df[0]:
        assemDirec="/work/GoryaninU/mitsuki/out/spades/mizuho/{}".format(assemname)
        scaffFilepath="{}/scaffolds.long.fasta".format(assemDirec)
        fl="{}/filtered/{}_R1.fastq".format(assemDirec, assemname)
        fr="{}/filtered/{}_R2.fastq".format(assemDirec, assemname)
        dbFilepath="/work/GoryaninU/mitsuki/bowtie/mizuho/{}".format(assemDirec)
        outFilepath="/work/GoryaninU/mitsuki/out/bowtie/mizuho/{}.sam".format(assemname)
        cmd="sbatch bowtie.sh {} {} {} {} {}".format(scaffFilepath, dbFilepath, fl, fr, outFilepath)
        myrun(cmd)

if __name__=="__main__":
    listFilepath="../assembly.list"
    main(listFilepath)
