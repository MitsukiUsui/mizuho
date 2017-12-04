#!/usr/bin/env python3

import os
import sys
import pandas as pd
from Bio import SeqIO

def main(listFilepath, baseDirec):
    """
    listFilepath: assemName,scaffoldFilepath
    baseDirec: each scaffold will be output to ${baseDirec}/${assemName}/${scaffname}/seq.fna
    """

    df=pd.read_csv(listFilepath)
    for _,row in df.iterrows():
        assemName=row["assembly_name"]
        inFilepath=row["scaffold_filepath"]
        print("START: {}".format(assemName))
        
        assemDirec="{}/{}".format(baseDirec, assemName)
        os.makedirs(assemDirec, exist_ok = True)
        
        for i,record in enumerate(SeqIO.parse(inFilepath, "fasta")):
            if len(record.seq)<100000:
                print("\tDONE: output {} scaffolds".format(i))
                break
            scaffname="sc{0:05d}".format(i + 1)
            outDirec="{}/{}".format(assemDirec, scaffname)
            os.makedirs(outDirec, exist_ok = True)
            outFilepath="{}/seq.fna".format(outDirec)
            SeqIO.write(record, outFilepath, "fasta")

if __name__=="__main__":
    listFilepath=sys.argv[1]
    baseDirec=sys.argv[2]
    main(listFilepath, baseDirec)
