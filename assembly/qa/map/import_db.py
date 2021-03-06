#!/usr/bin/env python3

import sys
import pandas as pd
import sqlite3
from Bio import SeqIO

from MapDbController import MapDbController

def parse_fastq(fastqFilepath):
    dct_lst=[]
    read2id={}
    for i,record in enumerate(SeqIO.parse(fastqFilepath, "fastq")):
        dct={"id":i, "name": record.id}
        dct_lst.append(dct)
        read2id[dct["name"]]=dct["id"]
    read_df=pd.DataFrame(dct_lst)
    read_df=read_df[["id", "name"]]
    return read_df, read2id

def parse_scaffold(scaffFilepath):
    dct_lst=[]
    scaff2id={"*":-1}
    for i,record in enumerate(SeqIO.parse(scaffFilepath, "fasta")):
        dct={"id":i, "name": record.id, "length": len(record.seq)}
        dct_lst.append(dct)
        scaff2id[dct["name"]]=dct["id"]
    scaff_df=pd.DataFrame(dct_lst)
    scaff_df=scaff_df[["id", "name", "length"]]
    return scaff_df, scaff2id
    
def parse_sam(samFilepath, read2id, scaff2id):
    dct_lst=[]
    with open(samFilepath, "r", errors="ignore") as f:
        for line in f:
            lineSplit=line.strip().split("\t")
            if line[0]!="@" and len(lineSplit)>=3:
                readName=lineSplit[0]
                scaffName=lineSplit[2]
                try:
                    dct={"read_id":read2id[readName], "scaff_id":scaff2id[scaffName]}
                    dct_lst.append(dct)
                except KeyError:
                    print("WARN: undefined {},{}".format(readName, scaffName))
    sam_df=pd.DataFrame(dct_lst)
    sam_df=sam_df[["read_id", "scaff_id"]]
    return sam_df
        
def main(dbFilepath, fastqFilepath, scaffFilepath, bowtieFilepath):
    mdc=MapDbController(dbFilepath)
   
    print("START: parse {}".format(fastqFilepath))
    read_df, read2id = parse_fastq(fastqFilepath)
    print("START: load {} records to {}".format(read_df.shape[0], dbFilepath))
    mdc.clear_row("read")
    read_df.to_sql("read", mdc.con, if_exists="append", index=False)
    
    print("START: parse {}".format(scaffFilepath))
    scaff_df, scaff2id = parse_scaffold(scaffFilepath)
    print("START: load {} records to {}".format(scaff_df.shape[0], dbFilepath))
    mdc.clear_row("scaffold")
    scaff_df.to_sql("scaffold", mdc.con, if_exists="append", index=False)
    
    print("START: parse {}".format(bowtieFilepath))
    bowtie_df = parse_sam(bowtieFilepath, read2id, scaff2id)
    print("START: load {} records to {}".format(bowtie_df.shape[0], dbFilepath))
    mdc.clear_row("bowtie")
    bowtie_df.to_sql("bowtie", mdc.con, if_exists="append", index=False)

if __name__=="__main__":
    dbFilepath=sys.argv[1]
    fastqFilepath=sys.argv[2]
    scaffFilepath=sys.argv[3]
    bowtieFilepath=sys.argv[4]
    main(dbFilepath, fastqFilepath, scaffFilepath, bowtieFilepath)
    
