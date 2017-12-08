#!/usr/bin/env python3

import pandas as pd
import sys
sys.path.append("/home/m/mitsuki-usui/mizuho/helper")
from helper import get_sampleId_lst

dbDirec="/work/GoryaninU/mitsuki/out/map/db"

pool_lst=["MFC1_36m_anode"]
for assemName in pool_lst:
    yamlFilepath="/home/m/mitsuki-usui/mizuho/assembly/spades/yaml/{}.yaml".format(assemName)
    sampleId_lst=get_sampleId_lst(yamlFilepath)
    for sampleId in sampleId_lst:
        dbFilepath="{}/{}/{}.sq3".format(dbDirec, assemName, sampleId)
        statFilepath=dbFilepath.replace(".sq3", ".stat")
        print("{},{}".format(dbFilepath, statFilepath))

pairFilepath="pair.list"
pair_df=pd.read_csv(pairFilepath)
for sampleId in pair_df["sample_id"]:
    dbFilepath="{0}/{1}/{1}.sq3".format(dbDirec, sampleId)
    statFilepath=dbFilepath.replace(".sq3", ".stat")
    print("{},{}".format(dbFilepath, statFilepath))
