#!/usr/bin/env python3

import os
from Bio import SeqIO
import pandas as pd

def main(listFilepath, baseDirec, outFilepath):
    df=pd.read_csv(listFilepath, header=None)
    print("START: merge")
    with open(outFilepath, "w") as fo:
        for assemname in df[0]:
            assemDirec="{}/{}".format(baseDirec, assemname)
            scaffname_lst=sorted([f.name for f in os.scandir(assemDirec) if f.is_dir()])
            for scaffname in scaffname_lst:
                inFilepath="{}/{}/genes.faa".format(assemDirec, scaffname)
                for i,record in enumerate(SeqIO.parse(inFilepath, "fasta")):
                    seqId="{0}:{1}:{2:04d}".format(assemname, scaffname, i + 1)
                    record.id=seqId
                    record.name=seqId
                    record.description=""
                    SeqIO.write(record, fo, "fasta")
            print("\t{}".format(assemDirec))
    print("DONE: output to {}".format(outFilepath))

if __name__=="__main__":
    listFilepath="../pool.list"
    baseDirec="/work/GoryaninU/mitsuki/out/taxonomy"
    
    outDirec="{}/mmseqs_pool".format(baseDirec)
    os.makedirs(outDirec, exist_ok=True)
    outFilepath="{}/merge.faa".format(outDirec)
    main(listFilepath, baseDirec, outFilepath)
