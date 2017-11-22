#!/usr/bin/env python3

import os
import yaml
import pandas as pd
from myutil.myutil import myrun

def get_sampleId_lst(yamlFilepath):
    with open(yamlFilepath, 'r') as f:
        yml=yaml.load(f)
    filepath_lst=yml[0]["left reads"] # assume all the same with yml[0]["right reads"]
    sampleId_lst=[filepath.split('/')[-1].replace(".fastq", "")[:-3]  for filepath in filepath_lst]
    return sampleId_lst

def main(assemListFilepath):
    assem_df=pd.read_csv(assemListFilepath, header=None)
    for _, row in assem_df.iterrows():
        if row[0]!="all":
            assemName=row[0]
            outFilepath="/work/GoryaninU/mitsuki/out/binning/bowtie/{}.bam".format(assemName)
            cmd="sbatch caller.sh {}".format(outFilepath)
            yamlFilepath="/home/m/mitsuki-usui/mizuho/assembly/spades/yaml/{}.yaml".format(assemName)
            sampleId_lst=get_sampleId_lst(yamlFilepath)
            for sampleId in sampleId_lst:
                bamFilepath="/work/GoryaninU/mitsuki/out/binning/bowtie/{}/{}.bam".format(sampleId, assemName)
                cmd += " " + bamFilepath
            #print(cmd)
            myrun(cmd)
            
if __name__=="__main__":
    assemListFilepath="../../list/assembly.list"
    main(assemListFilepath)
