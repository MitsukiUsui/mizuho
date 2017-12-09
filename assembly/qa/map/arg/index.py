#!/usr/bin/env python3

import pandas as pd

mapper="bwa"

pairFilepath="pair.list"
pair_df=pd.read_csv(pairFilepath)
ind_lst=list(pair_df["sample_id"])
pool_lst=["MFC1_36m_anode"]
assemName_lst = pool_lst + ind_lst

for assemName in assemName_lst:
    scaffFilepath="/work/GoryaninU/mitsuki/out/spades/mizuho/{}/scaffolds.fasta".format(assemName)
    dbFilepath="/work/GoryaninU/mitsuki/out/map/{}/index/{}".format(mapper, assemName)
    print("{},{},{}".format(mapper, scaffFilepath, dbFilepath))
