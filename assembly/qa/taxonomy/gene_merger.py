#!/usr/bin/env python3

import os
import sys
from Bio import SeqIO
import pandas as pd

def main(listFilepath, baseDirec, outFilepath):
    df=pd.read_csv(listFilepath)
    print("START: merge")
    with open(outFilepath, "w") as fo:
        for assemName in df["assembly_name"]:
            assemDirec="{}/{}".format(baseDirec, assemName)
            scaffName_lst=sorted([f.name for f in os.scandir(assemDirec) if f.is_dir()])
            for scaffName in scaffName_lst:
                inFilepath="{}/{}/genes.faa".format(assemDirec, scaffName)
                for i,record in enumerate(SeqIO.parse(inFilepath, "fasta")):
                    seqId="{0}:{1}:{2:04d}".format(assemName, scaffName, i + 1)
                    record.id=seqId
                    record.name=seqId
                    record.description=""
                    SeqIO.write(record, fo, "fasta")
            print("\t{}".format(assemDirec))
    print("DONE: output to {}".format(outFilepath))

if __name__=="__main__":
    listFilepath=sys.argv[1]
    baseDirec=sys.argv[2]
    mmseqsDirec="{}/mmseqs".format(baseDirec)
    os.makedirs(mmseqsDirec, exist_ok=True)
    outFilepath="{}/merge.faa".format(mmseqsDirec)
    main(listFilepath, baseDirec, outFilepath)
