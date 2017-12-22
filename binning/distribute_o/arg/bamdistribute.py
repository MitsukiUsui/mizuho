#!/usr/bin/env python3

import pandas as pd
import yaml

def get_sampleId_lst(yamlFilepath):
    with open(yamlFilepath, 'r') as f:
        yml=yaml.load(f)
    filepath_lst=yml[0]["left reads"] # assume all the same with yml[0]["right reads"]
    sampleId_lst=[filepath.split('/')[-1].replace(".fastq", "")[:-3]  for filepath in filepath_lst]
    return sampleId_lst

def main(assemListFilepath, numBins, metagenDirec):
    assem_df=pd.read_csv(assemListFilepath)
    
    for _, row in assem_df.iterrows():
        assemName=row["assembly_name"]
        sampleId_lst=get_sampleId_lst(row["yaml_filepath"])
        inFilepath_lst=["{}/bowtie/map/{}/{}.bam".format(metagenDirec, sampleId, assemName) for sampleId in sampleId_lst]
        mergeFilepath="{}/bowtie/map/{}.bam".format(metagenDirec, assemName)
        numBins=173
        print("{},{},{},{}".format(assemName, " ".join(inFilepath_lst), mergeFilepath, numBins))

if __name__=="__main__":
    assemListFilepath="../list/assembly.list"
    numBins=173
    metagenDirec="/work/GoryaninU/mitsuki/out/binning/metagen"
    main(assemListFilepath, numBins,metagenDirec)
