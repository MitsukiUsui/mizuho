#!/usr/bin/env python3

import pandas as pd
import sys
from myutil.myutil import myrun

def main(listFilepath):
    list_df=pd.read_csv(listFilepath, header=None)
    for _, row in list_df.iterrows():
        assemname=row[0]
        scaffFilepath=row[1]
        dbFilepath="/work/GoryaninU/mitsuki/bowtie/mizuho/{}".format(assemname)
        cmd="sbatch ../../index.sh {} {}".format(scaffFilepath, dbFilepath)
        myrun(cmd)

if __name__=="__main__":
    listFilepath="../../list/assembly.list"
    main(listFilepath)
