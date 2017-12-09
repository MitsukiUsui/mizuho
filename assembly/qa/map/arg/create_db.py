#!/usr/bin/env python3

import pandas as pd
import sys
sys.path.append("/home/m/mitsuki-usui/mizuho/helper")
from helper import get_sampleId_lst

dbDirec="/work/GoryaninU/mitsuki/out/map/db"

pool_lst=["MFC1_36m_anode"]
for assemName in pool_lst:
    scaffFilepath="/work/GoryaninU/mitsuki/out/spades/mizuho/{}/scaffolds.fasta".format(assemName)
    yamlFilepath="/home/m/mitsuki-usui/mizuho/assembly/spades/yaml/{}.yaml".format(assemName)
    sampleId_lst=get_sampleId_lst(yamlFilepath)
    for sampleId in sampleId_lst:
        dbFilepath="{}/{}/{}.sq3".format(dbDirec, assemName, sampleId)
        fastqFilepath="/work/GoryaninU/mitsuki/mizuho/dna/filter/{}_R1.fastq".format(sampleId)
        bowtieFilepath="/work/GoryaninU/mitsuki/out/map/bowtie/sam/{}/{}.sam".format(assemName, sampleId)
        bwaFilepath="/work/GoryaninU/mitsuki/out/map/bwa/sam/{}/{}.sam".format(assemName, sampleId)
        print("{},{},{},{},{}".format(dbFilepath, fastqFilepath, scaffFilepath, bowtieFilepath, bwaFilepath))

pairFilepath="pair.list"
pair_df=pd.read_csv(pairFilepath)
for sampleId in pair_df["sample_id"]:
    dbFilepath="{0}/{1}/{1}.sq3".format(dbDirec, sampleId)
    fastqFilepath="/work/GoryaninU/mitsuki/mizuho/dna/filter/{}_R1.fastq".format(sampleId)
    scaffFilepath="/work/GoryaninU/mitsuki/out/spades/mizuho/{}/scaffolds.fasta".format(sampleId)
    bowtieFilepath="/work/GoryaninU/mitsuki/out/map/bowtie/sam/{0}/{0}.sam".format(sampleId)
    bwaFilepath="/work/GoryaninU/mitsuki/out/map/bwa/sam/{0}/{0}.sam".format(sampleId)
    print("{},{},{},{},{}".format(dbFilepath, fastqFilepath, scaffFilepath, bowtieFilepath, bwaFilepath))
