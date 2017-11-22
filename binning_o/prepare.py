#!/usr/bin/env python3

import pandas as pd
from Bio import SeqIO
import os

def get_num_seqs(fastqFilepath):
    statsFilepath=fastqFilepath.replace(".fastq", ".stats")
    stats_df=pd.read_csv(statsFilepath, delimiter='\t')
    return stats_df["num_seqs"][0]

def main(metagenDirec, assemListFilepath, pairListFilepath):
    """
    output Countigs.fasta, count-map.tsv, reads_info.txt for MetaGen.R
    """

    os.makedirs("{}/contigs".format(metagenDirec), exist_ok=True)
    os.makedirs("{}/output".format(metagenDirec), exist_ok=True)
    contigFilepath="{}/contigs/Contigs.fasta".format(metagenDirec)
    tableFilepath="{}/output/count-map.tsv".format(metagenDirec)
    infoFilepath="{}/reads_info.txt".format(metagenDirec)

    assem_df=pd.read_csv(assemListFilepath, header=None)
    pair_df=pd.read_csv(pairListFilepath, header=None)
    
    # output Contigs.fasta
    print("START: concatenate contigs")
    contigCount_lst=[]
    assemName_lst=[]
    
    with open(contigFilepath, "w") as fo:
        for _, row in assem_df.iterrows():
            if row[0] != "all":
                seqFilepath=row[1]
                contigCount=0
                for record in SeqIO.parse(seqFilepath, "fasta"):
                    contigCount += 1
                    SeqIO.write(record, fo, "fasta")
                contigCount_lst.append(contigCount)
                assemName_lst.append(row[0])
                print("\tDONE: {} seqs from {}".format(contigCount, seqFilepath))
    print("DONE: output {}".format(contigFilepath))

    # summarize .count information to table_df
    print("START: summarize count")
    table_df=pd.DataFrame(index=range(sum(contigCount_lst)))
    for _, row in pair_df.iterrows():
        sampleId=row[0]
        table_lst=[]
        for assemName, contigCount in zip(assemName_lst, contigCount_lst):
            countFilepath="/work/GoryaninU/mitsuki/out/binning/bowtie/{}/{}.filter.count".format(sampleId, assemName)
            count_df=pd.read_csv(countFilepath, delimiter="\t", header=None)
            assert count_df.shape[0] == contigCount + 1 # +1 for unmapped last line 
            table_lst = table_lst + list(count_df[2][:-1])
        table_df[sampleId]=table_lst
        print("\tDONE: {}".format(sampleId))
    # output table_df to count-map.tsv
    table_df.to_csv(tableFilepath, index=False, sep='\t')
    print("DONE: output {}".format(tableFilepath))

    # output reads_info.txt
    dct_lst=[]
    for _, row in pair_df.iterrows():
        dct={}
        dct["filenames_1"]=row[1]
        dct["filenames_2"]=row[2]
        leftCount=get_num_seqs(row[1])
        rightCount=get_num_seqs(row[2])
        assert leftCount==rightCount
        dct["readcount_1"]=leftCount * 2
        dct_lst.append(dct)
    info_df=pd.DataFrame(dct_lst)
    info_df=info_df[["filenames_1", "filenames_2", "readcount_1"]]
    info_df.to_csv(infoFilepath, index=False)
    print("DONE: output {}".format(infoFilepath))

if __name__=="__main__":
    metagenDirec="/work/GoryaninU/mitsuki/out/binning/metagen/filter"
    assemListFilepath="./list/assembly.list"
    pairListFilepath="./list/pair.list"
    main(metagenDirec, assemListFilepath, pairListFilepath)
