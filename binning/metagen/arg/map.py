#!/usr/bin/env python3

import pandas as pd

def main(sampleListFilepath, assemListFilepath, metagenDirec):
    sample_df=pd.read_csv(sampleListFilepath)
    assem_df=pd.read_csv(assemListFilepath)
    
    for _, row in sample_df.iterrows():
        sampleId=row["sample_id"]
        leftFilepath=row["left_filepath"]
        rightFilepath=row["right_filepath"]

        for _, row in assem_df.iterrows():
            assemName=row["assembly_name"]
            dbFilepath="{}/bowtie/index/{}".format(metagenDirec, assemName)
            samFilepath="{}/bowtie/map/{}/{}.sam".format(metagenDirec, sampleId, assemName)
            print("{},{},{},{}".format(dbFilepath, leftFilepath, rightFilepath, samFilepath))

if __name__=="__main__":
    sampleListFilepath="./list/sample.list"
    assemListFilepath="./list/assembly.list"
    metagenDirec="/work/GoryaninU/mitsuki/out/binning/metagen"
    main(sampleListFilepath, assemListFilepath, metagenDirec)
