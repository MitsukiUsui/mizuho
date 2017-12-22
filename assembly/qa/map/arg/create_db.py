#!/usr/bin/env python3

import pandas as pd

sampleFilepath="sample.list"
assemFilepath="assembly.list"
sample_df=pd.read_csv(sampleFilepath)
assem_df=pd.read_csv(assemFilepath)
for _,row in sample_df.iterrows():
    sampleId=row["sample_id"]
    assemName=row["assembly_name"]

    dbFilepath="/work/GoryaninU/mitsuki/out/map/db/{}/{}.sq3".format(assemName, sampleId)
    fastqFilepath=row["left_filepath"]
    scaffFilepath=assem_df[assem_df["assembly_name"]==assemName]["scaffold_filepath"].iloc[0]
    bowtieFilepath="/work/GoryaninU/mitsuki/out/map/bowtie/sam/{}/{}.sam".format(assemName, sampleId)
    print("{},{},{},{}".format(dbFilepath, fastqFilepath, scaffFilepath, bowtieFilepath))
