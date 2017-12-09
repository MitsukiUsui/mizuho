#!/usr/bin/env python3

import pandas as pd

dbFilepath="/home/m/mitsuki-usui/mizuho/read/electgen/electgen"

seqDirec="/work/GoryaninU/mitsuki/mizuho/dna"
outDirec="/work/GoryaninU/mitsuki/out/electgen"
metaFilepath="mizuho_metadata_dna.csv"
meta_df=pd.read_csv(metaFilepath)
#for fastqId in meta_df["fastq_id"]:
#    #rowFilepath="{}/row/{}.fastq.gz".format(seqDirec, fastqId)
#    #outFilepath="{}/row/{}.m8".format(outDirec, fastqId)
#    #print("{},{},{}".format(dbFilepath, rowFilepath, outFilepath))
#    
#    filFilepath="{}/filter/{}.fastq".format(seqDirec, fastqId)
#    outFilepath="{}/filter/{}.m8".format(outDirec, fastqId)
#    print("{},{},{}".format(dbFilepath, filFilepath, outFilepath))

seqDirec="/work/GoryaninU/mitsuki/mizuho/rna"
outDirec="/work/GoryaninU/mitsuki/out/electgen/rna"
metaFilepath="mizuho_metadata_rna.csv"
meta_df=pd.read_csv(metaFilepath)
for fastqId in meta_df["fastq_id"]:
    rowFilepath="{}/row/{}.fastq.gz".format(seqDirec, fastqId)
    outFilepath="{}/row/{}.m8".format(outDirec, fastqId)
    print("{},{},{}".format(dbFilepath, rowFilepath, outFilepath))
