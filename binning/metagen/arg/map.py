#!/usr/bin/env python3

import sys
import pandas as pd

baseDirec=sys.argv[1]
assemListFilepath="assembly.list"
sampleListFilepath="sample.list"

assem_df=pd.read_csv(assemListFilepath)
sample_df=pd.read_csv(sampleListFilepath)

for assemName in assem_df["assembly_name"]:
    dbFilepath="{}/bowtie/index/{}".format(baseDirec, assemName)
    
    for _, row in sample_df.iterrows():
        sampleId=row["sample_id"]
        leftFilepath=row["left_filepath"]
        rightFilepath=row["right_filepath"]
        samFilepath="{}/bowtie/map/{}/{}.sam".format(baseDirec, assemName, sampleId)
        print("{},{},{},{}".format(dbFilepath, leftFilepath, rightFilepath, samFilepath))
