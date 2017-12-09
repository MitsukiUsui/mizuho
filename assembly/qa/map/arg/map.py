#!/usr/bin/env python3

import pandas as pd
import sys
sys.path.append("/home/m/mitsuki-usui/mizuho/helper")
from helper import get_sampleId_lst

mapper="bwa"
seqDirec="/work/GoryaninU/mitsuki/mizuho/dna/filter"
dbDirec="/work/GoryaninU/mitsuki/out/map/{}/index".format(mapper)
samDirec="/work/GoryaninU/mitsuki/out/map/{}/sam".format(mapper)

pool_lst=["MFC1_36m_anode"]
for assemName in pool_lst:
    dbFilepath="{}/{}".format(dbDirec, assemName)
    yamlFilepath="/home/m/mitsuki-usui/mizuho/assembly/spades/yaml/{}.yaml".format(assemName)
    sampleId_lst=get_sampleId_lst(yamlFilepath)
    for sampleId in sampleId_lst:
        leftFilepath="{}/{}_R1.fastq".format(seqDirec, sampleId)
        rightFilepath="{}/{}_R2.fastq".format(seqDirec, sampleId)
        samFilepath="{}/{}/{}.sam".format(samDirec, assemName, sampleId)
        print("{},{},{},{},{}".format(mapper, dbFilepath, leftFilepath, rightFilepath, samFilepath))

pairFilepath="pair.list"
pair_df=pd.read_csv(pairFilepath)
for sampleId in pair_df["sample_id"]:
    dbFilepath="{}/{}".format(dbDirec, sampleId)
    leftFilepath="{}/{}_R1.fastq".format(seqDirec, sampleId)
    rightFilepath="{}/{}_R2.fastq".format(seqDirec, sampleId)
    samFilepath="{0}/{1}/{1}.sam".format(samDirec, sampleId)
    print("{},{},{},{},{}".format(mapper, dbFilepath, leftFilepath, rightFilepath, samFilepath))
