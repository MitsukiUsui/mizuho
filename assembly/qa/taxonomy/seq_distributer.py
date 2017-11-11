#!/usr/bin/env python3

import os
import pandas as pd
from Bio import SeqIO

def main(listFilepath, baseDirec):
    """
    listFilepath: assemname,scaffoldFilepath
    baseDirec: each scaffold will be output to ${baseDirec}/${assemname}/${scaffname}/seq.fna
    """

    df=pd.read_csv(listFilepath, header=None)
    for _,row in df.iterrows():
        assemname=row[0]
        inFilepath=row[1]
        print("START: {}".format(assemname))
        
        assemDirec="{}/{}".format(baseDirec, assemname)
        os.makedirs(assemDirec)
        
        for i,record in enumerate(SeqIO.parse(inFilepath, "fasta")):
            if len(record.seq)<100000:
                print("\toutput {} scaffolds".format(i))
                break
            scaffname="sc{0:04d}".format(i + 1)
            outDirec="{}/{}".format(assemDirec, scaffname)
            os.makedirs(outDirec)
            outFilepath="{}/seq.fna".format(outDirec)
            SeqIO.write(record, outFilepath, "fasta")

if __name__=="__main__":
    listFilepath="assembly.list"
    baseDirec="/work/GoryaninU/mitsuki/out/taxonomy"
    main(listFilepath, baseDirec)
