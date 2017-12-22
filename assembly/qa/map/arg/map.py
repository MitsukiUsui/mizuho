#!/usr/bin/env python3

import pandas as pd

mapper="bowtie"
sampleFilepath="sample.list"
sample_df=pd.read_csv(sampleFilepath)

for _,row in sample_df.iterrows():
    dbFilepath="/work/GoryaninU/mitsuki/out/map/{}/index/{}".format(mapper, row["assembly_name"])
    samFilepath="/work/GoryaninU/mitsuki/out/map/{}/sam/{}/{}.sam".format(mapper, row["assembly_name"], row["sample_id"])
    print("{},{},{},{},{}".format(mapper, dbFilepath, row["left_filepath"], row["right_filepath"], samFilepath))
