#!/usr/bin/env python3

import sys
import pandas as pd

def main(baseDirec, assemListFilepath):
    assem_df=pd.read_csv(assemListFilepath)
    for _, row in assem_df.iterrows():
        assemName=row["assembly_name"]
        scaffFilepath=row["scaffold_filepath"]
        dbFilepath="{}/bowtie/index/{}".format(baseDirec, assemName)
        print("{},{}".format(scaffFilepath, dbFilepath))

if __name__=="__main__":
    baseDirec=sys.argv[1]
    assemListFilepath="assembly.list"
    main(baseDirec, assemListFilepath)
