#!/usr/bin/env python3

import pandas as pd
import sys

listFilepath=sys.argv[1]
baseDirec=sys.argv[2]
assem_df=pd.read_csv(listFilepath)
for assemName in assem_df["assembly_name"]:
    print("{}/{}".format(baseDirec, assemName))
