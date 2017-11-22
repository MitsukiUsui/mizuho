#!/usr/bin/env python3

import pandas as pd
from Bio import SeqIO
import os

def get_num_seqs(fastqFilepath):
    statsFilepath=fastqFilepath.replace(".fastq", ".stats")
    stats_df=pd.read_csv(statsFilepath, delimiter='\t')
    return stats_df["num_seqs"][0]

def main(sampleListFilepath, assemListFilepath, metagenDirec):
    """
    output Countigs.fasta, count-map.tsv, reads_info.txt for MetaGen.R
    """

    os.makedirs("{}/contigs".format(metagenDirec), exist_ok=True)
    os.makedirs("{}/output".format(metagenDirec), exist_ok=True)
    contigFilepath="{}/contigs/Contigs.fasta".format(metagenDirec)
    tableFilepath="{}/output/count-map.tsv".format(metagenDirec)
    infoFilepath="{}/reads_info.txt".format(metagenDirec)

    sample_df=pd.read_csv(sampleListFilepath)
    assem_df=pd.read_csv(assemListFilepath)
    
    # output Contigs.fasta
    print("START: concatenate contigs")
    contigCount_lst=[]
    
    with open(contigFilepath, "w") as fo:
        for _, row in assem_df.iterrows():
            seqFilepath=row[1]
            contigCount=0
            for record in SeqIO.parse(seqFilepath, "fasta"):
                contigCount += 1
                SeqIO.write(record, fo, "fasta")
            contigCount_lst.append(contigCount)
            print("\tDONE: {} seqs from {}".format(contigCount, seqFilepath))
    print("DONE: output {}".format(contigFilepath))

    # summarize .count information to table_df
    print("START: summarize count")
    table_df=pd.DataFrame(index=range(sum(contigCount_lst)))
    for _, row in sample_df.iterrows():
        sampleId=row["sample_id"]
        table_lst=[]
        for _, row in assem_df.iterrows():
            assemName=row["assembly_name"]
            countFilepath="{}/bowtie/map/{}/{}.count".format(metagenDirec, sampleId, assemName)
            count_df=pd.read_csv(countFilepath, delimiter="\t", header=None)
            assert count_df.shape[0] == contigCount_lst[_] + 1 # +1 for unmapped last line 
            table_lst = table_lst + list(count_df[2][:-1])
        table_df[sampleId]=table_lst
        print("\tDONE: {}".format(sampleId))
    # output table_df to count-map.tsv
    table_df.to_csv(tableFilepath, index=False, sep='\t')
    print("DONE: output {}".format(tableFilepath))

    # output reads_info.txt
    dct_lst=[]
    for _, row in sample_df.iterrows():
        dct={}
        dct["filenames_1"]=row["left_filepath"]
        dct["filenames_2"]=row["right_filepath"]
        leftCount=get_num_seqs(row["left_filepath"])
        rightCount=get_num_seqs(row["right_filepath"])
        assert leftCount==rightCount
        dct["readcount_1"]=leftCount * 2
        dct_lst.append(dct)
    info_df=pd.DataFrame(dct_lst)
    info_df=info_df[["filenames_1", "filenames_2", "readcount_1"]]
    info_df.to_csv(infoFilepath, index=False)
    print("DONE: output {}".format(infoFilepath))

if __name__=="__main__":
    sampleListFilepath="./list/sample.list"
    assemListFilepath="./list/assembly.list"
    metagenDirec="/work/GoryaninU/mitsuki/out/binning/metagen"
    main(sampleListFilepath, assemListFilepath, metagenDirec)
