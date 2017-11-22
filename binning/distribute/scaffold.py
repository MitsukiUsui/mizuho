#!/usr/bin/env python3

import pandas as pd
from Bio import SeqIO
import os

from distribute import get_result_df

def main(assemListFilepath, binningDirec):
    resultFilepath="{}/metagen/output/segs.txt".format(binningDirec)
    result_df=get_result_df(resultFilepath)
    scaffName2binId={}
    for scaffName, binId in zip(result_df["key"], result_df["bin_id"]):
        scaffName2binId[scaffName]=binId

    # distribute records to record_lstlst according to scaffName2binId 
    numBins=result_df["bin_id"].max()
    record_lstlst=[[] for _ in range(numBins)]    
    assem_df=pd.read_csv(assemListFilepath)
    for _, row in assem_df.iterrows():
        inFilepath=row["scaffold_filepath"]
        print("START: split {}".format(inFilepath))
        
        for record in SeqIO.parse(inFilepath, "fasta"):
            if record.id in scaffName2binId:
                binId=scaffName2binId[record.id]
                record_lstlst[binId - 1].append(record) ## record_lstlst is 0 origin
            else:
                print("\tERROR: unknown {}".format(record.id))
                   

    print("START: output into {} bins".format(numBins))
    for i, record_lst in enumerate(record_lstlst):
        binId = i + 1
        outDirec="{}/distribute/bin{:03d}".format(binningDirec, binId)
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
    assemListFilepath="../list/assembly.list"
    binningDirec="/work/GoryaninU/mitsuki/out/binning"
    main(assemListFilepath, binningDirec)
