#!/usr/bin/env python3

import pandas as pd
from Bio import SeqIO
import os

from distribute import get_result_df

def main(metagenDirec, binDirec):
    contigFilepath="{}/contigs/Contigs.fasta".format(metagenDirec)
    resultFilepath="{}/output/segs.txt".format(metagenDirec)
    
    result_df=get_result_df(resultFilepath)
    scaffName2binId={}
    for scaffName, binId in zip(result_df["key"], result_df["bin_id"]):
        scaffName2binId[scaffName]=binId

    # distribute records to record_lstlst according to scaffName2binId 
    numBins=result_df["bin_id"].max()
    record_lstlst=[[] for _ in range(numBins)]    
    for record in SeqIO.parse(contigFilepath, "fasta"):
        if record.id in scaffName2binId:
            binId=scaffName2binId[record.id]
            record_lstlst[binId - 1].append(record) ## record_lstlst is 0 origin
        else:
            print("\tERROR: unknown {}".format(record.id))

    print("START: output into {} bins".format(numBins))
    for i, record_lst in enumerate(record_lstlst):
        binId = i + 1
        outDirec="{}/bin{:03d}".format(binDirec, binId)
        os.makedirs(outDirec, exist_ok=True)
        outFilepath="{}/scaffolds.fasta".format(outDirec, binId)
        if os.path.exists(outFilepath):
            os.remove(outFilepath)

        print("\t{} seqs to {}".format(len(record_lst), outFilepath))
        with open(outFilepath, "a") as f:
            sorted_lst=sorted(record_lst, key=len, reverse=True)
            for record in sorted_lst:
                SeqIO.write(record, f, "fasta")

if __name__=="__main__":
    metagenDirec="/work/GoryaninU/mitsuki/out/metagen/MFC1_36m_anode"
    binDirec="/work/GoryaninU/mitsuki/out/bin"
    main(metagenDirec, binDirec)
