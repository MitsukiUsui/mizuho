#!/usr/bin/env python3

import pandas as pd

baseDirec="/work/GoryaninU/mitsuki/mizuho/dna"
pairFilepath="../pair.list"
pair_df=pd.read_csv(pairFilepath)
for _,row in pair_df.iterrows():
    sampleId=row["sample_id"]
    print("{},{}".format(baseDirec, sampleId))
