#!/usr/bin/env python3

import pandas as pd

def main(sampleListFilepath):
    sample_df=pd.read_csv(sampleListFilepath)
    for _, row in sample_df.iterrows():
        sampleId=row["sample_id"]
        print(sampleId)

if __name__=="__main__":
    sampleListFilepath="../list/sample.list"
    main(sampleListFilepath)
