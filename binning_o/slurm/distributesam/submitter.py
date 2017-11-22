#!/usr/bin/env python3

import pandas as pd
from myutil.myutil import myrun

def main(assemListFilepath):
    assem_df=pd.read_csv(assemListFilepath, header=None)
    for _, row in assem_df.iterrows():
        if row[0]!="all":
            assemName=row[0]
            cmd="sbatch caller.sh {}".format(assemName)
            print(cmd)
            #myrun(cmd)
            
if __name__=="__main__":
    assemListFilepath="../../list/assembly.list"
    main(assemListFilepath)
