#!/usr/bin/env python3

import pandas as pd
import sys
from myutil.myutil import myrun

def main(listFilepath):
    list_df=pd.read_csv(listFilepath, header=None)
    for assemname in list_df[0]:
        directory_lst=["/work/GoryaninU/mitsuki/mizuho/dna/row",
                       "/work/GoryaninU/mitsuki/mizuho/dna/trim",
                       "/work/GoryaninU/mitsuki/out/spades/mizuho/{}/filtered".format(assemname)]
        extension_lst=["fastq.gz", "fastq", "fastq"]
        
        for directory, extension in zip(directory_lst, extension_lst):
            for direction in ("R1", "R2"):
                seqFilepath="{}/{}_{}.{}".format(directory, assemname, direction, extension)
                statsFilepath="{}/{}_{}.stats".format(directory, assemname, direction)
                cmd = "sbatch stats.sh {} {}".format(seqFilepath, statsFilepath)
                myrun(cmd)

if __name__=="__main__":
    listFilepath="../assembly.list"
    main(listFilepath)
