#!/usr/bin/env python3

import os
import pandas as pd
from myutil.myutil import myrun

def main(pairListFilepath):
    pair_df=pd.read_csv(pairListFilepath, header=None)
    
    for _, row in pair_df.iterrows():
        sampleId=row[0]
        cmd="sbatch caller.sh {}".format(sampleId)
        myrun(cmd)
            
if __name__=="__main__":
    #pairListFilepath="../../list/pair.list"
    pairListFilepath="rerun.list"
    main(pairListFilepath)
