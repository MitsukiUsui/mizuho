#!/usr/bin/env python3

import sys
import pandas as pd
from Bio import SeqIO
import os

def get_num_seqs(fastqFilepath):
    statsFilepath=fastqFilepath.replace(".fastq", ".stat")
    stats_df=pd.read_csv(statsFilepath, delimiter='\t')
    return stats_df["num_seqs"][0]

def main(metagenDirec, sampleListFilepath, assemListFilepath):
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
                if len(record.seq) >= 10000:
                    contigCount += 1
                    SeqIO.write(record, fo, "fasta")
                else:
                    break
            contigCount_lst.append(contigCount)
            print("\tDONE: {} seqs from {}".format(contigCount, seqFilepath))
    print("DONE: output {}".format(contigFilepath))

    # summarize .count information to table_df
    column_lst=list(sample_df["sample_id"])
    table_df=pd.DataFrame(columns=column_lst)

    for i, assemName in enumerate(assem_df["assembly_name"]):
        subTable_df=pd.DataFrame(columns=column_lst)
        for sampleId in sample_df["sample_id"]:
            #countFilepath="{}/bowtie/map/{}/{}.count".format(metagenDirec, assemName, sampleId)
            countFilepath="/work/GoryaninU/mitsuki/out/map/bowtie/sam/{}/{}.count".format(assemName, sampleId)
            count_df=pd.read_csv(countFilepath, delimiter="\t", header=None)

            count_lst=[]
            for _, row in count_df.iterrows():
                if row[1]>=10000:
                    count_lst.append(row[2])
                else:
                    break ##assuming count file is descending order
            assert len(count_lst)==contigCount_lst[i]
            subTable_df[sampleId]=count_lst
        table_df=pd.concat([table_df, subTable_df])
    table_df=table_df[column_lst].astype(int)
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
    baseDirec=sys.argv[1]
    sampleListFilepath="sample.list"
    assemListFilepath="assembly.list"
    main(baseDirec, sampleListFilepath, assemListFilepath)
