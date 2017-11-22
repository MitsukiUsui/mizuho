#!/usr/bin/env python3

import pandas as pd

def main(assemListFilepath, metagenDirec):
    assem_df=pd.read_csv(assemListFilepath)
    for _, row in assem_df.iterrows():
        assemName=row["assembly_name"]
        scaffFilepath=row["scaffold_filepath"]
        dbFilepath="{}/bowtie/index/{}".format(metagenDirec, assemName)
        print("{},{}".format(scaffFilepath, dbFilepath))

if __name__=="__main__":
    assemListFilepath="./list/assembly.list"
    metagenDirec="/work/GoryaninU/mitsuki/out/binning/metagen"
    main(assemListFilepath, metagenDirec)
