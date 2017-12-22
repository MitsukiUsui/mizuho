#!/usr/bin/env python3

import pandas as pd

def main(sampleListFilepath, binningDirec):
    sample_df=pd.read_csv(sampleListFilepath)
    
    for _, row in sample_df.iterrows():
        dbFilepath="{}/distribute/bowtie/index/all".format(binningDirec)
        leftFilepath=row["left_filepath"]
        rightFilepath=row["right_filepath"]
        samFilepath="{}/distribute/bowtie/map/{}.sam".format(binningDirec, row["sample_id"])
        print("{},{},{},{}".format(dbFilepath, leftFilepath, rightFilepath, samFilepath))

if __name__=="__main__":
    sampleListFilepath="../list/sample.list"
    binningDirec="/work/GoryaninU/mitsuki/out/binning"
    main(sampleListFilepath, binningDirec)
